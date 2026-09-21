# -*- coding: utf-8 -*-

import time
import threading

import numpy as np
import serial.tools.list_ports

from rplidar import RPLidar
from sklearn.cluster import DBSCAN

from config import (
    ZONE_COUNT,
    ZONE_BOUNDS,
    LIDAR_MIN_DISTANCE_MM,
    LIDAR_MAX_DISTANCE_MM,
)


class LiDARThread:

    def __init__(
        self,
        port=None,
        min_d=LIDAR_MIN_DISTANCE_MM,
        max_d=LIDAR_MAX_DISTANCE_MM
    ):

        self.port = port or self._find_port()

        self.lidar = RPLidar(self.port)

        self.min_d = min_d
        self.max_d = max_d

        self.running = False
        self.ready = False

        self.dist_zones = [None] * ZONE_COUNT

        self.last_update = time.time()

    def _find_port(self):

        for port_info in serial.tools.list_ports.comports():

            device = port_info.device.lower()

            if "usb" in device or "ttyusb" in device:
                print(
                    f"[LiDAR] USB port bulundu: {port_info.device}"
                )

                return port_info.device

        raise RuntimeError("LiDAR port not found!")

    def start(self):

        self.running = True

        thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        thread.start()

    def _run(self):

        try:

            print("[LiDAR] Motor başlatılıyor...")

            self.lidar.start_motor()

            self.ready = True

            print("[LiDAR] LiDAR hazır.")

            for scan in self.lidar.iter_scans():

                if not self.running:
                    break

                zones = {
                    i: []
                    for i in range(ZONE_COUNT)
                }

                for _, angle, distance in scan:

                    if not (
                        self.min_d
                        <= distance
                        <= self.max_d
                    ):
                        continue

                    # Forward field of view
                    if not (
                        120 <= angle <= 240
                    ):
                        continue

                    for i in range(ZONE_COUNT):

                        lower = ZONE_BOUNDS[i]
                        upper = ZONE_BOUNDS[i + 1]

                        if i == ZONE_COUNT - 1:

                            if lower <= angle <= upper:

                                zones[i].append(
                                    (distance, angle)
                                )

                                break

                        else:

                            if lower <= angle < upper:

                                zones[i].append(
                                    (distance, angle)
                                )

                                break

                self.last_update = time.time()

                new_distances = []

                for points in zones.values():

                    if not points:

                        new_distances.append(None)

                        continue

                    arr = np.array(points)

                    X = np.stack(
                        [
                            arr[:, 0]
                            * np.cos(
                                np.radians(arr[:, 1])
                            ),

                            arr[:, 0]
                            * np.sin(
                                np.radians(arr[:, 1])
                            )
                        ],
                        axis=1
                    )

                    labels = DBSCAN(
                        eps=150,
                        min_samples=3
                    ).fit_predict(X)

                    min_distance = None

                    for label in set(labels):

                        if label == -1:
                            continue

                        group = arr[
                            labels == label
                        ]

                        distance = group[:, 0].mean()

                        if (
                            min_distance is None
                            or distance < min_distance
                        ):
                            min_distance = distance

                    if min_distance is not None:

                        new_distances.append(
                            min_distance / 1000.0
                        )

                    else:

                        new_distances.append(None)

                self.dist_zones = new_distances

        except Exception as e:

            print(
                f"[LiDAR ERROR] {e}"
            )

            self.ready = False

        finally:

            try:

                self.lidar.stop_motor()
                self.lidar.disconnect()

            except Exception:
                pass

            print("[LiDAR] Thread sonlandırıldı.")

    def stop(self):

        self.running = False
