# Fire and Flame Detection System using CNN and ESP32-CAM

This project aims to build a real-time fire and flame detection system using Convolutional Neural Networks (CNN) with TensorFlow/Keras. The system utilizes the ESP32-CAM module for video streaming and connects to a server via WiFi. The server processes the camera feed, detects fire/flame, and sends notifications to trigger an alarm when a fire is detected.

## Features

- **Real-time video streaming** from ESP32-CAM.
- **Fire and flame detection** using a CNN model trained with TensorFlow/Keras.
- **Server communication** for receiving camera input and sending responses.
- **Notification system** to trigger an alarm or action when fire is detected.
- **WiFi connectivity** to transmit data between ESP32-CAM and the server.
- **Alarm system** that activates in response to fire detection.

## Architecture

1. **ESP32-CAM**: Captures real-time video footage and streams it to the server over WiFi.
2. **Server**: 
    - Receives the video stream from ESP32-CAM.
    - Uses a pre-trained CNN model for fire detection.
    - Sends a response back to the ESP32-CAM to trigger alarms and notifications.
3. **CNN Model**: A TensorFlow/Keras-based CNN model trained to detect fire/flames in the camera footage.
4. **Alarm System**: The server triggers an alarm (e.g., sound, notification) when fire is detected.

## Project Setup

### 1. ESP32-CAM Setup

1. Install the required libraries and drivers to program the ESP32-CAM.
2. Configure the ESP32-CAM to connect to your WiFi network and stream video to the server.
3. Upload the code to the ESP32-CAM to start streaming.

### 2. Server Setup

1. **Install Dependencies**:
   - Python 3.x
   - TensorFlow
   - Flask or FastAPI (for handling requests from ESP32-CAM)
   - OpenCV (for video processing)
   - Requests library (for handling HTTP requests)
   ```bash
   pip install tensorflow flask opencv-python requests
