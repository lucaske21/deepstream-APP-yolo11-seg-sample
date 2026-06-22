cmake_minimum_required(VERSION 3.16)
project(nvdsparse_yolo_instance_mask LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(NOT DEFINED ENV{DEEPSTREAM_SDK_PATH})
  set(DEEPSTREAM_SDK_PATH /opt/nvidia/deepstream/deepstream)
else()
  set(DEEPSTREAM_SDK_PATH $ENV{DEEPSTREAM_SDK_PATH})
endif()

include_directories(
  ${DEEPSTREAM_SDK_PATH}/sources/includes
  ${CMAKE_CURRENT_SOURCE_DIR}
)

add_library(nvdsparse_yolo_instance_mask SHARED
  nvdsparse_yolo_instance_mask.cpp
)

target_compile_options(nvdsparse_yolo_instance_mask PRIVATE -Wall -Wextra -Wpedantic)
