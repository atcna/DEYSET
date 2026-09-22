# Jetson Setup

This document describes the software environment required to run the DEYSET perception pipeline on NVIDIA Jetson hardware.

## Hardware Platform

The system was developed and tested on:

- NVIDIA Jetson Orin Nano Super 8GB
- IMX219 wide-angle camera
- RPLIDAR A1M8
- RFbeam K-MD2 24 GHz FMCW radar
- SH1106 OLED display
- Nextion display
- RC522 RFID reader

## NVIDIA Software Stack

The DEYSET processing pipeline uses the following NVIDIA software environment:

- NVIDIA JetPack 6.2
- L4T 36.4.3
- Ubuntu 22.04
- CUDA 12.6
- cuDNN 9.3
- TensorRT 10.3
- NVIDIA DeepStream 7.1
- GStreamer

## Python Environment

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```
```markdown
Install the Python dependencies:

```bash
pip install -r requirements.txt
```
```markdown
## DeepStream Python Integration

The DEYSET object detection pipeline uses NVIDIA DeepStream and GStreamer for real-time video processing and neural-network inference.

The Python application interacts with the DeepStream pipeline through the DeepStream Python bindings (`pyds`).

The DeepStream pipeline integrates camera acquisition, stream multiplexing, neural-network inference, video conversion, on-screen display, and frame access.
