cmake_minimum_required(VERSION 3.18)

project(DEYSET
    VERSION 1.0
    DESCRIPTION "Real-Time Multi-Sensor Perception"
    LANGUAGES C CXX
)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# NVIDIA DeepStream installation for your Jetpack
set(DEEPSTREAM_DIR "/opt/nvidia/deepstream/deepstream"
    CACHE PATH "Path to NVIDIA DeepStream installation"
)

message(STATUS "DEYSET CMake configuration")
message(STATUS "DeepStream path: ${DEEPSTREAM_DIR}")

# verify deepStream installation
if(NOT EXISTS "${DEEPSTREAM_DIR}")
    message(WARNING
        "NVIDIA DeepStream was not found at ${DEEPSTREAM_DIR}. "
        "This project is intended to be built on NVIDIA Jetson hardware "
        "with DeepStream installed."
    )
else()
    message(STATUS "DeepStream installation found.")
endif()

# Project directories
set(DEYSET_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src")
set(DEYSET_WEB_DIR "${CMAKE_CURRENT_SOURCE_DIR}/web")
set(DEYSET_CONFIG_DIR "${CMAKE_CURRENT_SOURCE_DIR}/config")

message(STATUS "Source directory: ${DEYSET_SOURCE_DIR}")
message(STATUS "Web directory: ${DEYSET_WEB_DIR}")

# native DeepStream components can be added here when required.
#
# for example:
# add_subdirectory(src/native)
#
# python-based deepStream processing is handled separately through
# the deepStream python bindings with (pyds).
