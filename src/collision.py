# -*- coding: utf-8 -*-

import time
import threading

from firebase import send_collision_event
from display import (
    blink_nextion_p1,
    blink_oled_collision,
)
_detection_active = False
_detection_start_time = 0.0

_detection_lock = threading.Lock()

def trigger_collision_warning(
    duration=3.0
):

    global _detection_active
    global _detection_start_time
    with _detection_lock:

        if _detection_active:
            return

        _detection_active = True

        _detection_start_time = time.time()

    print(
        "[COLLISION] Risk detected!"
    )
    # Firebase
    send_collision_event()

    # Nextion
    threading.Thread(
        target=blink_nextion_p1,
        args=(duration,),
        daemon=True
    ).start()

    # OLED + Buzzer
    threading.Thread(
        target=blink_oled_collision,
        args=(duration,),
        daemon=True
    ).start()

    threading.Thread(
        target=_reset_detection,
        args=(duration,),
        daemon=True
    ).start()


def _reset_detection(
    duration
):
    global _detection_active

    time.sleep(duration)

    with _detection_lock:

        _detection_active = False
def is_collision_active():
    with _detection_lock:
        return _detection_active
