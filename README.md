# DEYSET

## Real-Time Multi-Sensor Perception and Collision Risk Detection System for Automotive Applications

DEYSET is a real-time automotive perception and collision risk detection system developed as a multi-sensor ADAS research project at Çankaya University.

The project was conducted as an undergraduate research project under the TÜBİTAK 2209-B program and was carried out over approximately 1–2 years. The project also included technical interaction and industry-oriented collaboration with SDT Space & Defense Technologies.

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
### Operating System and NVIDIA Platform
- Ubuntu 22.04
- NVIDIA JetPack 6.2
- L4T 36.4.3
- CUDA 12.6
- cuDNN 9.3
- TensorRT 10.3
- DeepStream 7.1

### Programming and Processing
- Python
- C/C++
- NumPy
- SciPy
- scikit-learn
- OpenCV

### Computer Vision
- YOLO-based object detection
- NVIDIA DeepStream
- NVIDIA TensorRT

### Sensor Processing
- RPLIDAR A1M8
- RFbeam K-MD2 FMCW radar
- DBSCAN-based LiDAR clustering
- Range-Doppler processing

### Monitoring
- Firebase Realtime Database
- Flask
- HTML/CSS/JavaScript
## Multi-Sensor Perception
DEYSET uses complementary information from camera, LiDAR, and radar sensors to improve real-time environmental perception.

The camera provides visual object information, while LiDAR provides distance measurements and the 24 GHz FMCW radar provides range and velocity-related information.

The sensor information is spatially associated using predefined angular zones. This allows detected objects to be evaluated together with distance and motion information obtained from the corresponding sensing regions


## Object Detection
The camera stream is processed using NVIDIA DeepStream for real-time object detection.

The system detects the following object classes:
- Vehicle
- Bicycle
- Person
- Road Sign
The camera pipeline operates at a resolution of 1280 × 720 with a target frame rate of 30 FPS.
Object detections provide class and image-position information that is used in the subsequent sensor correlation and collision-risk detection stages.


## LiDAR Processing
The RPLIDAR A1M8 is used to obtain 2D distance measurements from the surrounding environment.
The LiDAR processing pipeline includes:

- Serial device detection
- LiDAR scan acquisition
- Angular filtering
- Spatial clustering
- Minimum-distance estimation
- Angular-zone association
The system uses DBSCAN clustering to group spatially related LiDAR measurements and estimate the distance of detected objects within the defined sensing regions.
  

## Radar Processing
The RFbeam K-MD2 24 GHz FMCW radar is used as an additional sensing modality for detecting objects and obtaining range and velocity-related information.
The radar communicates with the NVIDIA Jetson platform over Ethernet.
The processing pipeline includes:
- TCP communication with the radar
- Radar data acquisition
- Range-Doppler data processing
- Detection extraction
- Dynamic-target filtering
- Range and velocity estimation
- Angular-zone association

Radar measurements provide complementary information to the camera and LiDAR, particularly for estimating the motion-related characteristics of detected targets.

## Sensor Correlation
Camera detections are correlated with measurements obtained from the corresponding LiDAR and radar sensing zones.
The system uses predefined angular regions to associate sensor measurements with detected objects.
This approach allows visual detections to be evaluated together with spatial and motion-related sensor information rather than relying solely on camera-based observations.


## Collision Risk Detection
DEYSET evaluates potential collision-risk situations by combining object detection results with distance and sensor information.
When a detected person or other relevant object enters a predefined risk region, the system evaluates the available sensor measurements to determine whether a warning condition should be triggered.
When a collision-risk condition is detected, the system can activate:
- OLED visual warning
- Nextion display warning
- Audible buzzer
- Firebase event logging

The warning event is recorded in Firebase Realtime Database for subsequent monitoring and analysis.
## Firebase and Web Dashboard
DEYSET uses Firebase Realtime Database for storing selected system events and session information.

A Flask-based web dashboard provides access to the recorded information.
- The dashboard includes:
- Driver/session records
- Session logs
- Date-based log inspection
- Collision-risk events
- Driver performance information

The web interface is separated from the real-time perception pipeline and communicates with the Firebase database.

## Publications and Performance Analysis
### 1.Real-Time Object Detection for Automotive Systems With FMCW Radar-Based Sensor Fusion

- 27th International Radar Symposium (IRS 2026)
- Kraków, Poland, 19–21 May 2026
- Authors: Atacan Akpınar, Doğa Tik, Berke Özbay, Beyza Nur Erkan, Elif Aydın

- This work presents a radar-centric multi-sensor perception framework combining FMCW radar, camera-based deep learning detections, and LiDAR-based spatial ranging for real-time collision-risk assessment. The study focuses on Doppler-derived radial velocity and radar-assisted target association.

- DOI: 10.23919/IRS70539.2026.11548965
- IEEE Xplore
### 2.Enhanced Object Detection for Vehicle Safety through Multi-Sensor Fusion

- 2025 16th International Conference on Electrical and Electronics Engineering (ELECO 2025)
- Bursa, Türkiye, 2025
- Authors: Beyza Nur Erkan, Atacan Akpınar, Berke Özbay, Doğa Tik, Elif Aydın

- This work presents the DEYSET multi-sensor ADAS framework, combining camera-based object detection, LiDAR-based ranging, and FMCW radar sensing for real-time object detection and collision-risk assessment.
- IEEE Xplore
## Usage

The general system workflow is:

1. Connect the sensors
2. Initialize the LiDAR
3. Initialize the radar
4. Initialize the camera
5. Start the DeepStream pipeline
6. Detect objects
7. Process LiDAR and radar measurements
8. Correlate sensor information
9. Evaluate collision risk
10. Trigger warnings
11. Log events to Firebase


## Installation
The main processing system is designed for NVIDIA Jetson hardware with the required NVIDIA software stack installed.

1. Clone the repository
```bash
git clone https://github.com/atcna/DEYSET.git
cd DEYSET
```
2. Create a Python environment where appropriate:
```python3 -m venv venv
source venv/bin/activate
```
3. Install the Python dependencies:
```pip install -r requirements.txt
```
Hardware-specific components such as NVIDIA DeepStream, Jetson.GPIO, camera drivers, and LiDAR/radar interfaces may require platform-specific installation steps.

Detailed setup instructions will be provided in:
docs/setup_jetson.md

## Configuration 
Sensitive credentials and configuration files are intentionally excluded from this repository.

Examples include:
- Firebase service-account credentials
- API keys
- Passwords
- Secret keys
- Local hardware-specific configuration

Use the example configuration files provided in the repository and configure the system locally.
