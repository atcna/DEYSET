# DEYSET

## Real-Time Multi-Sensor Perception and Collision Risk Detection System for Automotive Applications

DEYSET is a real-time automotive perception and collision risk detection system developed as a multi-sensor ADAS research project.

The system combines camera-based object detection with LiDAR and FMCW radar sensing to improve environmental perception and identify potential collision-risk situations.

The project was developed on an NVIDIA Jetson Orin Nano Super platform and integrates computer vision, LiDAR processing, radar signal processing, sensor fusion, real-time visualization, and cloud-based monitoring.

---

## System Overview

The system combines multiple sensing technologies to provide real-time environmental perception:

- Camera-based object detection
- 2D LiDAR distance measurement
- 24 GHz FMCW radar sensing
- Multi-sensor spatial correlation
- Collision-risk detection
- Real-time warning mechanisms
- Firebase-based event logging
- Web-based monitoring dashboard

The general processing flow is:

```text
                    ┌─────────────────────┐
                    │   Camera / IMX219   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Object Detection    │
                    │   YOLO / DeepStream │
                    └──────────┬──────────┘
                               │
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
 ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
 │ RPLIDAR A1M8   │   │ RFbeam K-MD2   │   │ Camera Object  │
 │ 2D LiDAR       │   │ 24 GHz FMCW    │   │ Information    │
 └───────┬────────┘   │ Radar          │   └───────┬────────┘
         │            └───────┬────────┘           │
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
                    ┌─────────────────────┐
                    │ Sensor Correlation  │
                    │ & Risk Assessment   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Collision Warning   │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
          OLED             Nextion           Buzzer
                               │
                               ▼
                         Firebase
                               │
                               ▼
                       Web Dashboard
Hardware

The prototype was developed using the following hardware:

Component	Description
NVIDIA Jetson Orin Nano Super	Main processing platform
IMX219	Wide-angle camera
RPLIDAR A1M8	2D LiDAR
RFbeam K-MD2	24 GHz FMCW radar
SH1106	OLED display
Nextion	Serial display
RC522	RFID reader
Buzzer	Audible warning mechanism




Software Stack
Operating System and NVIDIA Platform
Ubuntu 22.04
NVIDIA JetPack 6.2
L4T 36.4.3
CUDA 12.6
cuDNN 9.3
TensorRT 10.3
DeepStream 7.1
Programming and Processing
Python
C/C++
NumPy
SciPy
scikit-learn
OpenCV
Computer Vision
YOLO-based object detection
NVIDIA DeepStream
NVIDIA TensorRT
Sensor Processing
RPLIDAR A1M8
RFbeam K-MD2 FMCW radar
DBSCAN-based LiDAR clustering
Range-Doppler processing
Monitoring
Firebase Realtime Database
Flask
HTML/CSS/JavaScript

Multi-Sensor Perception

DEYSET uses complementary information from camera, LiDAR, and radar sensors.

The camera provides visual object information, while LiDAR provides distance measurements and radar provides range and velocity-related information.

The sensor information is associated spatially using predefined angular zones.

This allows detected objects to be evaluated together with measurements from the corresponding sensing region.

Object Detection

The camera stream is processed using NVIDIA DeepStream.

The current system uses the following object classes:

Vehicle
Bicycle
Person
Road sign

The camera pipeline processes a 1280 × 720 video stream at 30 FPS.

The object detection stage provides object class and image-position information that is subsequently used by the sensor correlation and collision-risk detection stages.

LiDAR Processing

The RPLIDAR A1M8 is used to obtain 2D distance measurements.

The LiDAR processing pipeline includes:

Serial device detection
LiDAR scan acquisition
Angular filtering
Spatial clustering
Distance estimation
Sensor-zone association

DBSCAN clustering is used to group LiDAR measurements into spatial clusters.

Radar Processing

The RFbeam K-MD2 24 GHz FMCW radar is connected to the Jetson platform through Ethernet.

The radar processing pipeline includes:

TCP communication
Radar data acquisition
Range-Doppler data processing
Detection extraction
Dynamic-target filtering
Distance and velocity estimation
Angular-zone association

Radar measurements are used as complementary information to the camera and LiDAR measurements.

Collision Risk Detection

Collision-risk detection combines object detection and distance information from the available sensors.

When a potentially hazardous situation is identified, the system can activate:

OLED warning
Nextion display warning
Audible buzzer
Firebase event logging

The warning event is also recorded for later analysis through the web dashboard.

Web Dashboard

DEYSET includes a Flask-based monitoring interface connected to Firebase Realtime Database.

The dashboard provides functionality for:

Driver/session records
Event logs
Collision-risk records
Date-based log inspection
Driver performance information

The web interface is separated from the real-time Jetson processing code.
