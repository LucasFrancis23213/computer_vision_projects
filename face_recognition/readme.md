# Face Recognition Project

This project uses the `face_recognition` and `OpenCV` libraries to load images, encode faces, and find the best match between test images and a sample image dataset.

## Project Structure

- **`FaceRecognitionMain.py`**: The main script for loading images, encoding them, and performing face recognition.
- **`samples/`**: A directory containing the sample images used for comparison.
- **`test_image/`**: A directory containing the test images to be recognized.

## Requirements

- `Python 3.11.5`
- `opencv-python`
- `numpy`
- `face_recognition`

### Installing Requirements

You can install the required packages by running the following command:

```bash
pip install -r requirement.txt
```
## Features

- Loads and resizes images from two directories: one for sample images and one for test images.
- Encodes the face landmarks using the `face_recognition` library.
- Compares the test images to the sample images to find the closest match.
- Displays both the test image and its best match from the sample dataset.

## How to Run
- Place your sample images in the ``samples/ directory``.
- Place your test images in the ``test_image/ directory``.
- Run the script:  
```bash
python FaceRecognitionMain.py
```
- The script will open windows displaying each test image along with its best match from the sample dataset.

## Notes
- Ensure that each image contains **at least one** recognizable face.
- All images are resized to **640x480** resolution to ensure uniformity during processing.

## Sample Encoding and Matching
The script uses the following steps for recognition:
- Image Loading: Loads the sample and test images and converts them to RGB.
- Encoding: Encodes the facial features of each image using face_recognition.face_encodings().
- Distance Calculation: Uses face_recognition.face_distance() to compute the Euclidean distance between the encodings of the test images and the sample images.
- Result Display: Displays the best matching sample image next to the test image for easy comparison.

## Exiting
> Press the ``ESC`` key to close the image windows and exit the program.  