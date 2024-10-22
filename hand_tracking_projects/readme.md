# Hand Gesture Recognition Projects

This folder contains two Python projects utilizing hand gesture recognition to perform specific tasks. These projects make use of the `cv2` library (OpenCV) and `mediapipe` for hand tracking and recognition, and additionally interface with system audio control.

## Project 1: Hand Tracking

**File**: `HandTrackingMain.py`

### Overview

This project tracks hands and detects key hand landmarks using the MediaPipe library. The script captures the video feed, processes each frame to detect hands, and draws the landmarks on the screen.

### Features

- Hand detection and tracking using MediaPipe.
- Real-time display of hand landmarks on the video feed.
- Customizable detection and tracking confidence levels.



## Project 2: Volume Control via Hand Gestures

**File**: `VolumeHandControl.py`

### Overview

This project allows controlling the system's volume by measuring the distance between the thumb and index finger using hand gesture recognition. The closer the fingers are, the lower the volume, and vice versa.

### Features

- Detects the thumb and index finger using hand landmarks.
- Calculates the distance between these two points and maps it to the system's volume range.
- Displays a volume control bar and the percentage of the current volume in real-time.

## How to Use

1. Install the required libraries:
   ```bash
   pip install -r requirement.txt
2. run the code:
   ```bash
   python HandTrackingMain.py  
