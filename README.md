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
