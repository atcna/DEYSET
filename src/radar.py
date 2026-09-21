# -*- coding: utf-8 -*-

import socket
import struct
import time
import threading

import numpy as np

from scipy.signal import find_peaks
from scipy.ndimage import uniform_filter

from config import (
    RADAR_IP,
    RADAR_PORT,
    RADAR_N,
    STATIC_SPEED_BIN,
    MIN_DYNAMIC_SPEED,
    MIN_AMPLITUDE_DB,
    RADAR_RANGE_RESOLUTION,
    RADAR_VELOCITY_RESOLUTION,
    RADAR_ANGLE_RESOLUTION,
)


radar_targets = []

radar_lock = threading.Lock()


def connect_radar():

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.connect(
        (
            RADAR_IP,
            RADAR_PORT
        )
    )

    print(
        f"[RADAR] Connected to "
        f"{RADAR_IP}:{RADAR_PORT}"
    )

    return sock


def recv_exact(sock, nbytes):

    buffer = b""

    while len(buffer) < nbytes:

        chunk = sock.recv(
            nbytes - len(buffer)
        )

        if not chunk:
            return None

        buffer += chunk

    return buffer


def parse_packet(sock):

    header = recv_exact(
        sock,
        4
    )

    if not header:
        return None, None

    length_data = recv_exact(
        sock,
        4
    )

    if not length_data:
        return None, None

    length = struct.unpack(
        "<I",
        length_data
    )[0]

    payload = recv_exact(
        sock,
        length
    )

    return (
        header.decode(
            "ascii",
            errors="ignore"
        ),
        payload
    )


def radar_thread():

    global radar_targets

    while True:

        sock = None

        try:

            print("[RADAR] Connecting...")

            sock = connect_radar()

            sock.sendall(
                b"INIT"
                + struct.pack("<I", 4)
                + struct.pack("<I", 3)
            )

            time.sleep(0.1)

            sock.sendall(
                b"DSF1"
                + struct.pack("<I", 4)
                + b"RMRD"
            )

            print(
                "[RADAR] Radar stream started."
            )

            while True:

                header, payload = parse_packet(
                    sock
                )

                if (
                    header != "RMRD"
                    or payload is None
                ):
                    continue

                data = np.frombuffer(
                    payload,
                    dtype=np.uint32
                )

                if data.size != RADAR_N * RADAR_N:
                    continue

                rd_map = (
                    10
                    * np.log10(
                        data.reshape(
                            (
                                RADAR_N,
                                RADAR_N
                            )
                        )
                        + 1e-6
                    )
                )

                rd_map = uniform_filter(
                    rd_map,
                    size=(5, 5),
                    mode="nearest"
                )

                min_bin = int(
                    0.5
                    / RADAR_RANGE_RESOLUTION
                )

                max_bin = int(
                    50.0
                    / RADAR_RANGE_RESOLUTION
                )

                detections = []

                for r in range(
                    min_bin,
                    min(
                        max_bin,
                        RADAR_N
                    )
                ):

                    peaks, _ = find_peaks(
                        rd_map[r],
                        height=MIN_AMPLITUDE_DB
                    )

                    for peak in peaks:

                        if abs(
                            peak
                            - STATIC_SPEED_BIN
                        ) < 2:

                            continue

                        detections.append(
                            (
                                r,
                                peak,
                                rd_map[r, peak]
                            )
                        )

                detections.sort(
                    key=lambda x: x[2],
                    reverse=True
                )

                targets = []

                for (
                    range_bin,
                    speed_bin,
                    amplitude
                ) in detections[:10]:

                    distance = (
                        range_bin
                        * RADAR_RANGE_RESOLUTION
                    )

                    speed = (
                        speed_bin
                        - STATIC_SPEED_BIN
                    ) * RADAR_VELOCITY_RESOLUTION

                    azimuth = (
                        speed_bin
                        - STATIC_SPEED_BIN
                    ) * RADAR_ANGLE_RESOLUTION

                    if (
                        abs(speed)
                        < MIN_DYNAMIC_SPEED
                    ):
                        continue

                    targets.append(
                        {
                            "distance": distance,
                            "speed": speed,
                            "azimuth": azimuth,
                            "amplitude": amplitude
                        }
                    )

                with radar_lock:

                    radar_targets.clear()

                    radar_targets.extend(
                        targets
                    )

        except Exception as e:

            print(
                f"[RADAR ERROR] {e}"
            )

            with radar_lock:
                radar_targets.clear()

            time.sleep(2)

        finally:

            if sock:

                try:
                    sock.close()

                except Exception:
                    pass


def get_radar_targets():

    with radar_lock:

        return radar_targets.copy()
