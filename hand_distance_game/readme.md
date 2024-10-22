# Hand Distance Game Project

This project is an interactive game that uses hand gesture recognition to measure the distance between the hand and the camera. The player interacts with a button displayed on the screen using hand gestures. The project utilizes `OpenCV` and `cvzone` for hand detection and tracking, and it calculates real-world hand distances to simulate a button pressing interaction.

## Features

- **Hand Detection**: Detects and tracks a single hand using the `cvzone.HandTrackingModule`.
- **Distance Calculation**: Calculates the real-world distance between two points on the hand to simulate interaction.
- **Interactive Game**: A button is displayed on the screen, and the player must move their hand close to the button to "press" it.
- **Score and Timer**: Keeps track of the player’s score and limits the game to a 30-second duration.
- **Real-Time Feedback**: Displays the distance between the hand and the camera, as well as the player’s score and remaining time.

## Requirements

- `Python 3.11`
- `opencv-python`
- `cvzone`
- `numpy`

### Installing Requirements

You can install the required packages by running the following command:  
```bash
pip install -r requirement.txt
```


## How to Run
- Ensure your webcam is connected.
- Run the script:
```bash
python hand_distance_game.py  
```
- A window will open where you can interact with the game using your hand.
- Move your hand toward the button displayed on the screen to "press" it. The closer your hand gets to the button, the higher your score.

## Game Instructions
- The goal of the game is to press the on-screen button using your hand before the time runs out.
- A new button will appear at random locations after each successful press.
- Your score and remaining time are displayed on the screen.

## Exiting the Game
- The game will automatically exit when the 30-second timer runs out.
- You can also manually exit by pressing the ESC key
