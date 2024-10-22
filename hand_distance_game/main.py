import math
import random
import time
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cv2


def camera_settings(screen_width: int = 1280, screen_height: int = 720):
    camera = cv2.VideoCapture(0)
    camera.set(3, screen_width)
    camera.set(4, screen_height)
    return camera


def calculate_distance(landmark_list):
    if len(landmark_list) != 0:
        marker_5 = landmark_list[5]
        marker_17 = landmark_list[17]
        distance = math.sqrt((marker_5[0] - marker_17[0]) ** 2 + (marker_5[1] - marker_17[1]) ** 2)
        # print(f"current distance on my hand is {int(distance)}")
        return int(distance)


def customize_hand_size_to_realworld_distance(distance, coff):
    A, B, C = coff
    result = A * distance ** 2 + B * distance + C
    # print(f"hand distance to camera is {int(result)}")
    return int(result)


def add_game_hud(image, time, score):
    cvzone.putTextRect(img=image, text=f'time is {time}',pos=(1000, 75), offset=20, thickness=1)
    cvzone.putTextRect(img=image, text=f'score is {score}', pos=(60, 75), offset=20, thickness=1)


def create_button(image, center_x, center_y, color=(255, 255, 0)):
    cv2.circle(image, (center_x, center_y), radius=35, thickness=cv2.FILLED, color=color)
    cv2.circle(image, (center_x, center_y), radius=10, thickness=cv2.FILLED, color=(255, 255, 255))
    cv2.circle(image, (center_x, center_y), radius=20, thickness=2, color=(255, 255, 0))
    # cv2.circle(image, (center_x, center_y), radius=30, thickness=cv2.FILLED, color=(50, 50, 50))


def main():
    hand_detector = HandDetector(maxHands=1, detectionCon=0.75)
    camera = camera_settings()

    x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
    y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    coff = np.polyfit(x, y, 2)
    # 游戏相关的变量
    color = (255, 255, 0)
    center_x, center_y = 250,250
    total_time, score = 30, 0
    time_start = time.time()
    counter = 0

    while True:
        capture_succeed, image = camera.read()
        image = cv2.flip(image, 1)
        hand, image = hand_detector.findHands(img=image, draw=True)

        if hand:
            landmark_list = hand[0]['lmList']
            hand_x, hand_y, hand_width, hand_height = hand[0]['bbox']
            hand_distance = calculate_distance(landmark_list)
            real_world_distance = customize_hand_size_to_realworld_distance(hand_distance, coff)
            cvzone.putTextRect(image, f'current distance is {real_world_distance} cm',
                               pos=(hand_x, hand_y), scale=2, thickness=1)
            if real_world_distance < 40:
                if hand_x < center_x < hand_x + hand_width and hand_y < center_y < hand_y + hand_height:
                    counter = 1

        if counter:
            counter += 1
            color = (0, 255, 0)
            if counter >= 4:
                counter = 0
                center_x, center_y = random.randint(100,900), random.randint(90, 600)
                color = (0, 255, 0)
                score += 1

        create_button(image, center_x, center_y, color)
        color = (255, 0, 255)

        used_time = int(time.time() - time_start)
        add_game_hud(image, total_time - used_time, score)
        cv2.imshow("hand distance game", image)
        if cv2.waitKey(1) & 0xFF == 27 or used_time >= total_time:
            break


if __name__ == "__main__":
    main()