# -*- coding: utf-8 -*-

import time
import serial

import Jetson.GPIO as GPIO

from PIL import Image, ImageDraw, ImageFont

from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

from config import (
    NEXTION_PORT,
    NEXTION_BAUDRATE,
    OLED_I2C_PORT,
    OLED_I2C_ADDRESS,
    BUZZER_GPIO_PIN,
)
# ============================================================
# GPIO
# ============================================================

GPIO.setmode(GPIO.BOARD)

GPIO.setup(
    BUZZER_GPIO_PIN,
    GPIO.OUT
)

GPIO.output(
    BUZZER_GPIO_PIN,
    GPIO.LOW
)
# ============================================================
# Nextion
# ============================================================

uart = serial.Serial(
    NEXTION_PORT,
    baudrate=NEXTION_BAUDRATE,
    timeout=1
)
def send_nextion_cmd(command):
    try:
        uart.write(
            command.encode("utf-8")
            + b"\xFF\xFF\xFF"
        )
        print(
            f"[Nextion] {command}"
        )
    except Exception as e:

        print(
            f"[Nextion ERROR] {e}"
        )
def blink_nextion_p1(
    duration=3
):

    send_nextion_cmd(
        "page five"
    )

    end_time = (
        time.time()
        + duration
    )

    visible = True

    while time.time() < end_time:

        send_nextion_cmd(
            f"vis p1,{1 if visible else 0}"
        )

        visible = not visible

        time.sleep(1)

    send_nextion_cmd(
        "vis p1,0"
    )
# ============================================================
# OLED
# ============================================================

i2c_serial = i2c(
    port=OLED_I2C_PORT,
    address=OLED_I2C_ADDRESS
)

oled = sh1106(
    i2c_serial
)


font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/"
    "DejaVuSans-Bold.ttf",
    18
)


triangle_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/"
    "DejaVuSans.ttf",
    28
)


def draw_warning_triangle(draw):

    outer = [
        (64, 10),
        (94, 50),
        (34, 50)
    ]

    inner = [
        (64, 15),
        (89, 48),
        (39, 48)
    ]

    draw.polygon(
        outer,
        outline=255,
        fill=255
    )

    draw.polygon(
        inner,
        outline=0,
        fill=0
    )

    draw.line(
        [64, 20, 64, 38],
        fill=255,
        width=2
    )

    draw.rectangle(
        (62, 42, 66, 46),
        fill=255
    )
def display_collision_warning():
    try:
        image = Image.new(
            "1",
            (
                oled.width,
                oled.height
            )
        )
        draw = ImageDraw.Draw(
            image
        )

        draw_warning_triangle(
            draw
        )

        oled.display(
            image
        )

    except Exception as e:

        print(
            f"[OLED ERROR] {e}"
        )
def clear_oled():
    try:
        oled.clear()
    except Exception as e:
        print(
            f"[OLED CLEAR ERROR] {e}"
        )
def activate_buzzer():
    GPIO.output(
        BUZZER_GPIO_PIN,
        GPIO.HIGH
    )
def deactivate_buzzer():

    GPIO.output(
        BUZZER_GPIO_PIN,
        GPIO.LOW
    )

def blink_oled_collision(
    duration=3
):

    end_time = (
        time.time()
        + duration
    )

    while time.time() < end_time:

        display_collision_warning()

        activate_buzzer()

        time.sleep(0.5)

        clear_oled()

        deactivate_buzzer()

        time.sleep(0.5)

def shutdown_display():

    try:

        deactivate_buzzer()

        clear_oled()

        uart.close()

        GPIO.cleanup()

    except Exception:
        pass
