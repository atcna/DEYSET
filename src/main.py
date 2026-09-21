# -*- coding: utf-8 -*-

import sys
import time
import threading
# DeepStream Python bindings
sys.path.append(
    "/opt/nvidia/deepstream/"
    "deepstream-7.1/"
    "sources/"
    "deepstream_python_apps"
)
import gi

gi.require_version(
    "Gst",
    "1.0"
)
from gi.repository import (
    GLib,
    Gst
)
import pyds
from common.platform_info import PlatformInfo
from common.bus_call import bus_call
from config import (
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    CAMERA_FPS,
    CAMERA_SENSOR_ID,
    CAMERA_SENSOR_MODE,
    CAMERA_HFOV,
    ZONE_COUNT,
    ZONE_BOUNDS,
    RADAR_ZONE_INDEX,
    PERSON_COLLISION_DISTANCE_M,
    DEEPSTREAM_PGIE_CONFIG,
    PGIE_CLASS_ID_PERSON,
)
from lidar import LiDARThread
from radar import (
    radar_thread,
    get_radar_targets,
)
from collision import (
    trigger_collision_warning,
)
# ============================================================
# Global state
# ============================================================

frame_counter = 0
fps_lock = threading.Lock()
lidar_thread = None

# ===========================================================
# FPS Monitor
# ============================================================
def fps_monitor():
    global frame_counter
    while True:
        time.sleep(10)
        with fps_lock:
            fps = (
                frame_counter
                / 10.0
            )
            print(
                f"[FPS] Last 10s: "
                f"{fps:.2f}"
            )
            frame_counter = 0
# ============================================================
# DeepStream OSD Probe
# ============================================================

def osd_sink_pad_buffer_probe(
    pad,
    info,
    u_data
):
    global frame_counter

    with fps_lock:

        frame_counter += 1

    buf = info.get_buffer()
    if not buf:
        return Gst.PadProbeReturn.OK
    batch_meta = (
        pyds.gst_buffer_get_nvds_batch_meta(
            hash(buf)
        )
    )
    frame_meta_list = (
        batch_meta.frame_meta_list
    )
    while frame_meta_list:
        frame_meta = (
            pyds.NvDsFrameMeta.cast(
                frame_meta_list.data
            )
        )
        frame_meta_list = (
            frame_meta_list.next
        )
        frame_width = (
            frame_meta.source_frame_width
        )
        object_list = (
            frame_meta.obj_meta_list
        )
        radar_targets = (
            get_radar_targets()
        )
        person_close = False
        radar_index = 0
        while object_list:

            obj_meta = (
                pyds.NvDsObjectMeta.cast(
                    object_list.data
                )
            )
            # ----------------------------------------
            # Object center
            # ----------------------------------------
            center_x = (
                obj_meta.rect_params.left
                + obj_meta.rect_params.width / 2
            )

            full_angle = (
                center_x
                / frame_width
                * CAMERA_HFOV
                + 120
            )
            # ----------------------------------------
            # Determine sensor zone
            # ----------------------------------------
            lidar_zone = None
            radar_zone = False

            for i in range(ZONE_COUNT):

                lower = ZONE_BOUNDS[i]
                upper = ZONE_BOUNDS[i + 1]

                if (
                    i == ZONE_COUNT - 1
                    and lower
                    <= full_angle
                    <= upper
                ):

                    if i == RADAR_ZONE_INDEX:
                        radar_zone = True

                    else:
                        lidar_zone = i

                    break
                elif (
                    i < ZONE_COUNT - 1
                    and lower
                    <= full_angle
                    < upper
                ):

                    if i == RADAR_ZONE_INDEX:
                        radar_zone = True

                    else:
                        lidar_zone = i

                    break
            # ----------------------------------------
            # Object label
            # ----------------------------------------

            label_text = (
                obj_meta.obj_label
            )
            text_lines = []
            # ----------------------------------------
            # LiDAR information
            # ----------------------------------------
            if (
                lidar_zone is not None
                and lidar_thread is not None
                and obj_meta.class_id
                == PGIE_CLASS_ID_PERSON
            ):
                if (
                    0
                    <= lidar_zone
                    < len(
                        lidar_thread.dist_zones
                    )
                ):
                    distance = (
                        lidar_thread
                        .dist_zones[
                            lidar_zone
                        ]
                    )
                    if distance is not None:
                        label_text += (
                            f" "
                            f"(LiDAR: "
                            f"{distance:.1f}m)"
                        )
                        if (
                            distance
                            < PERSON_COLLISION_DISTANCE_M
                        ):
                            person_close = True
            # ----------------------------------------
            # Radar information
            # ----------------------------------------
            if (
                radar_zone
                and radar_index
                < len(radar_targets)
            ):

                target = (
                    radar_targets[
                        radar_index
                    ]
                )

                distance = target[
                    "distance"
                ]

                speed = target[
                    "speed"
                ]

                azimuth = target[
                    "azimuth"
                ]

                text_lines.append(
                    f"Radar: D:{distance:.1f}m"
                )

                text_lines.append(
                    f"V:{speed:.1f}km/h"
                )

                text_lines.append(
                    f"A:{azimuth:.1f}°"
                )

                obj_meta.rect_params.border_width = 4

                radar_index += 1
            # ----------------------------------------
            # Display metadata
            # ---------------------------------------
            display_meta = (
                pyds
                .nvds_acquire_display_meta_from_pool(
                    batch_meta
                )
            )
            display_meta.num_labels = (
                1 + len(text_lines)
            )

            for i, line in enumerate(
                text_lines
            ):
              
                text_params = (
                    display_meta
                    .text_params[i]
                )

                text_params.display_text = (
                    line
                )

                text_params.x_offset = int(
                    obj_meta.rect_params.left
                )

                text_params.y_offset = max(
                    0,
                    int(
                        obj_meta.rect_params.top
                    )
                    - 16
                    - (
                        len(text_lines) - i
                    ) * 14
                )
                text_params.font_params.font_name = (
                    "Serif"
                )
                text_params.font_params.font_size = 12

                text_params.font_params.font_color.set(
                    1.0,
                    1.0,
                    0.0,
                    1.0
                )
                text_params.set_bg_clr = 1

                text_params.text_bg_clr.set(
                    0.0,
                    0.0,
                    0.0,
                    0.5
                )
            label = (
                display_meta
                .text_params[
                    len(text_lines)
                ]
            )
            label.display_text = (
                label_text
            )
            label.x_offset = int(
                obj_meta.rect_params.left
            )
            label.y_offset = max(
                0,
                int(
                    obj_meta.rect_params.top
                ) - 16
            )

            label.font_params.font_name = (
                "Serif"
            )
            label.font_params.font_size = 12

            label.font_params.font_color.set(
                1.0,
                1.0,
                1.0,
                1.0
            )
            label.set_bg_clr = 1

            label.text_bg_clr.set(
                0.0,
                0.0,
                0.0,
                0.5
            )
            pyds.nvds_add_display_meta_to_frame(
                frame_meta,
                display_meta
            )
            object_list = (
                object_list.next
            )
        # ----------------------------------------
        # Collision warning
        # ----------------------------------------
        if person_close:
            trigger_collision_warning(
                duration=3.0
            )

    return Gst.PadProbeReturn.OK
# ============================================================
# DeepStream Pipeline
# ============================================================
def main():
    global lidar_thread
    print(
        "[INFO] Starting radar thread..."
    )

    threading.Thread(
        target=radar_thread,
        daemon=True
    ).start()

    print(
        "[INFO] Starting FPS monitor..."
    )

    threading.Thread(
        target=fps_monitor,
        daemon=True
    ).start()

    Gst.init(None)

    loop = GLib.MainLoop()

    pipeline = Gst.Pipeline()

    platform = PlatformInfo()
    # -------------------------------------------------------
    # Camera
    # --------------------------------------------------------
    source = Gst.ElementFactory.make(
        "nvarguscamerasrc",
        "csi-source"
    )
    source.set_property(
        "sensor-id",
        CAMERA_SENSOR_ID
    )
    source.set_property(
        "sensor-mode",
        CAMERA_SENSOR_MODE
    )
    # --------------------------------------------------------
    # Camera Caps
    # --------------------------------------------------------
    caps = Gst.ElementFactory.make(
        "capsfilter",
        "src-caps"
    )
    caps.set_property(
        "caps",
        Gst.Caps.from_string(
            f"video/x-raw(memory:NVMM), "
            f"width={CAMERA_WIDTH}, "
            f"height={CAMERA_HEIGHT}, "
            f"format=NV12, "
            f"framerate={CAMERA_FPS}/1"
        )
    )
    # --------------------------------------------------------
    # Video Converter
    # --------------------------------------------------------
    vidconv_src = (
        Gst.ElementFactory.make(
            "nvvideoconvert",
            "nvvidconv_src"
        )
    )
    # --------------------------------------------------------
    # Streammux
    # --------------------------------------------------------
    streammux = (
        Gst.ElementFactory.make(
            "nvstreammux",
            "stream-muxer"
        )
    )
    streammux.set_property(
        "width",
        CAMERA_WIDTH
    )
    streammux.set_property(
        "height",
        CAMERA_HEIGHT
    )
    streammux.set_property(
        "batch-size",
        1
    )
    streammux.set_property(
        "batched-push-timeout",
        4000000
    )
    # --------------------------------------------------------
    # YOLO / Primary Inference
    # --------------------------------------------------------
    pgie = (
        Gst.ElementFactory.make(
            "nvinfer",
            "primary-inference"
        )
    )
    if not pgie:
        sys.stderr.write(
            "[ERROR] Could not create nvinfer.\n"
        )
        sys.exit(1)
    pgie.set_property(
        "config-file-path",
        DEEPSTREAM_PGIE_CONFIG
    )
    # --------------------------------------------------------
    # Post-processing
    # --------------------------------------------------------
    vidconv_post = (
        Gst.ElementFactory.make(
            "nvvideoconvert",
            "nvvidconv_post"
        )
    )
    nvosd = (
        Gst.ElementFactory.make(
            "nvdsosd",
            "onscreendisplay"
        )
    )
    # --------------------------------------------------------
    # Sink
    # --------------------------------------------------------

    sink = Gst.ElementFactory.make(
        (
            "nveglglessink"
            if platform.is_platform_aarch64()
            else "nvvideo-renderer"
        ),
        "nvvideo-renderer"
    )
    sink.set_property(
        "sync",
        False
    )
    elements = [
        source,
        caps,
        vidconv_src,
        streammux,
        pgie,
        vidconv_post,
        nvosd,
        sink
    ]
    for element in elements:
        if not element:
            sys.stderr.write(
                "[ERROR] "
                "GStreamer element could not "
                "be created.\n"
            )
            sys.exit(1)
        pipeline.add(element)
    # --------------------------------------------------------
    # Pipeline Linking
    # --------------------------------------------------------
    source.link(caps)
    caps.link(
        vidconv_src
    )
    srcpad = (
        vidconv_src
        .get_static_pad("src")
    )
    sinkpad = (
        streammux
        .get_request_pad("sink_0")
    )
    srcpad.link(
        sinkpad
    )
    streammux.link(
        pgie
    )
    pgie.link(
        vidconv_post
    )
    vidconv_post.link(
        nvosd
    )
    nvosd.link(
        sink
    )
    # --------------------------------------------------------
    # Bus
    # --------------------------------------------------------
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect(
        "message",
        bus_call,
        loop
    )
    # --------------------------------------------------------
    # OSD Probe
    # --------------------------------------------------------
    osd_pad = (
        nvosd.get_static_pad(
            "sink"
        )
    )
    osd_pad.add_probe(
        Gst.PadProbeType.BUFFER,
        osd_sink_pad_buffer_probe,
        0
    )
    # --------------------------------------------------------
    # Start
    # --------------------------------------------------------
    print(
        "[INFO] Starting DeepStream pipeline..."
    )
    pipeline.set_state(
        Gst.State.PLAYING
    )
    try:
        loop.run()
    except KeyboardInterrupt:

        print(
            "[INFO] Keyboard interrupt."
        )
    finally:
        print(
            "[INFO] DeepStream shutting down..."
        )
        pipeline.set_state(
            Gst.State.NULL
        )
 # ============================================================
# Entry Point
# ============================================================
if __name__ == "__main__":

    print(
        "======================================"
    )
    print(
        " DEYSET Multi-Sensor ADAS"
    )
    print(
        " Jetson Orin Nano Super"
    )
    print(
        "======================================"
    )
    # --------------------------------------------------------
    # LiDAR
    # --------------------------------------------------------
    print(
        "[INFO] Starting LiDAR..."
    )
    lidar_thread = None
    for attempt in range(1, 6):
        try:
            print(
                f"[INFO] LiDAR starting "
                f"(Attempt {attempt}/5)"
            )
            lidar_thread = (
                LiDARThread()
            )
            lidar_thread.start()
            for _ in range(10):
                if (
                    lidar_thread.ready
                    and any(
                        distance is not None
                        for distance
                        in lidar_thread.dist_zones
                    )
                ):
                    print(
                        "[LiDAR] Ready "
                        "and receiving data."
                    )
                    break
                print(
                    "[LiDAR] Waiting for data..."
                )
                time.sleep(0.5)
            else:
                raise RuntimeError(
                    "LiDAR started but "
                    "no data received."
                )
            break
        except Exception as e:
            print(
                f"[LiDAR ERROR] {e}"
            )

            time.sleep(2)
    else:
        print(
            "[ERROR] LiDAR failed "
            "after 5 attempts."
        )
        sys.exit(1)
    # --------------------------------------------------------
    # Firebase
    # --------------------------------------------------------
    try:
        from firebase import (
            initialize_firebase
        )

        initialize_firebase()
    except Exception as e:
        print(
            f"[FIREBASE ERROR] {e}"
        )

        print(
            "[WARNING] "
            "System will continue without "
            "Firebase."
        )
    # --------------------------------------------------------
    # DeepStream
    # --------------------------------------------------------
    try:
        print(
            "[INFO] Starting DeepStream..."
        )
        main()
    except Exception as e:
        print(
            f"[FATAL ERROR] {e}"
        )
        if lidar_thread:
            lidar_thread.stop()
        sys.exit(1)
