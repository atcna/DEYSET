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
```

## Hardware

| Component                     | Description               |
| ----------------------------- | ------------------------- |
| NVIDIA Jetson Orin Nano Super | Main processing platform  |
| IMX219                        | Wide-angle camera         |
| RPLIDAR A1M8                  | 2D LiDAR                  |
| RFbeam K-MD2                  | 24 GHz FMCW radar         |
| SH1106                        | OLED display              |
| Nextion                       | Serial display            |
| RC522                         | RFID reader               |
| Buzzer                        | Audible warning mechanism |

## Software Stack
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

