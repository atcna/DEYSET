# -*- coding: utf-8 -*-

# ============================================================
# DEYSET - System Configuration
# ============================================================

# ---------------- Camera ----------------
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_FPS = 30
CAMERA_SENSOR_ID = 0
CAMERA_SENSOR_MODE = 3
CAMERA_HFOV = 120.0


# ---------------- LiDAR ----------------
LIDAR_MIN_DISTANCE_MM = 100
LIDAR_MAX_DISTANCE_MM = 15000

ZONE_COUNT = 5

# Camera/LiDAR angular zones
ZONE_BOUNDS = [120, 144, 168, 192, 216, 240]

# Radar-associated zone
RADAR_ZONE_INDEX = 2


# ---------------- Radar ----------------
RADAR_IP = "192.168.16.2"
RADAR_PORT = 6172

RADAR_N = 256
STATIC_SPEED_BIN = RADAR_N // 2

RADAR_CLOCK = 38461538
RADAR_SCLK = 12

MIN_DYNAMIC_SPEED = 0.4
MIN_AMPLITUDE_DB = 10.0

# Radar range/velocity resolution.
# Update these values according to the RFbeam K-MD2 configuration.
RADAR_RANGE_RESOLUTION = 0.1
RADAR_VELOCITY_RESOLUTION = 0.1
RADAR_ANGLE_RESOLUTION = 1.0


# ---------------- Nextion ----------------
NEXTION_PORT = "/dev/ttyTHS1"
NEXTION_BAUDRATE = 9600


# ---------------- OLED ----------------
OLED_I2C_PORT = 7
OLED_I2C_ADDRESS = 0x3C


# ---------------- Buzzer ----------------
BUZZER_GPIO_PIN = 15


# ---------------- Collision Detection ----------------
PERSON_COLLISION_DISTANCE_M = 1.5
COLLISION_WARNING_DURATION = 3.0


# ---------------- Firebase ----------------
FIREBASE_JSON = "/home/deyset/deyset.json"

FIREBASE_URL = (
    "https://jetson-deyset-default-rtdb."
    "europe-west1.firebasedatabase.app/"
)


# ---------------- YOLO classes ----------------
PGIE_CLASS_ID_VEHICLE = 0
PGIE_CLASS_ID_BICYCLE = 1
PGIE_CLASS_ID_PERSON = 2
PGIE_CLASS_ID_ROADSIGN = 3


# ---------------- DeepStream ----------------
DEEPSTREAM_PGIE_CONFIG = "dstest1_pgie_config.txt"
