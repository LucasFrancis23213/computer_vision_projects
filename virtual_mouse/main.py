import cv2
import mediapipe
import math
import numpy as np
import time
import Projects.hand_tracking_projects.HandTrackingMain as htm
import pyautogui

def camera_settings(camera, camera_width: int = 1280, camera_height: int = 720):
    camera.set(3, camera_width)
    camera.set(4, camera_height)

def display_fps(image, previous_time):

    current_time = time.time()
    fps = 1 / (current_time - previous_time)

    # 将当前的fps呈现出来
    cv2.putText(image, f'press "esc" to quit current fps is {int(fps)}', (40, 70),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 1)
    return image, current_time


class VirtualMouse:
    def __init__(self, hand_detector: htm.HandIdentifier, initial_mouse_location: list, click_threshold = 60, smoothing_factor = 0.2):
        self.hand_detector = hand_detector
        self.landmarks: list = []
        self.index_finger, self.middle_finger, self.fingers_up = [],[],[]
        self.prev_mouse_location = initial_mouse_location
        # 两指间隔小于多少像素时会被识别为单击/双击
        self.click_threshold = click_threshold
        # 平滑系数，越小移动越慢
        self.smoothing_factor = smoothing_factor

    def get_landmarks(self, image: cv2.Mat):
        # step 1: get hand landmarks
        image = self.hand_detector.findHands(image=image)
        self.landmarks = self.hand_detector.findPosition(image=image)
        # print(self.landmarks)
        return image

    def get_index_and_middle_finger(self):
        # step 2: get index and middle finger position
        if len(self.landmarks) > 0:
            self.index_finger = self.landmarks[8][1:3]
            self.middle_finger = self.landmarks[12][1:3]
        else:
            return None

    def detect_fingers_Up(self):
        # step 3: detect which fingers are up
        # 获取手部关键点位置
        if len(self.landmarks) > 0:
            self.fingers_up.clear()
            # 先检查大拇指
            thumb_tip = self.landmarks[4]
            thumb_mcp = self.landmarks[2]
            if thumb_tip[1] < thumb_mcp[1]:
                self.fingers_up.append(1)
            else:
                self.fingers_up.append(0)

            for tip_id in [8,12,16,20]:
                tip = self.landmarks[tip_id]
                pp = self.landmarks[tip_id - 2]
                if tip[2] < pp[2]:
                    self.fingers_up.append(1)
                else:
                    self.fingers_up.append(0)
        print(self.fingers_up)

    @staticmethod
    def set_moving_mode(self) -> bool:
        if len(self.fingers_up) > 0:
            return self.fingers_up[1] == 1 and self.fingers_up[2] == 0

    @staticmethod
    def set_left_click_mode(self) -> bool:
        if len(self.fingers_up) > 0:
            return self.fingers_up[1] == 1 and self.fingers_up[2] == 1

    @staticmethod
    def set_right_click_mode(self) -> bool:
        if len(self.fingers_up) > 0:
            return self.fingers_up[0] == 1 and self.fingers_up[2] == 1
    @staticmethod
    def find_distance(self):
        if len(self.index_finger) > 0 and len(self.middle_finger) > 0:
            x = self.index_finger[0] - self.middle_finger[0]
            y = self.index_finger[1] - self.middle_finger[1]
            length = math.hypot(x, y)
            return length

    @staticmethod
    def change_coordinates(self, camera_width: int, camera_height: int):
        screen_width, screen_height = pyautogui.size()
        print(f"index finger is {self.index_finger}")
        x = np.interp(self.index_finger[0], (0, camera_width), (0, screen_width))
        y = np.interp(self.index_finger[1], (0, camera_height), (0, screen_height))
        return [x, y]

    @staticmethod
    def smoothening_mouse_move(self, target_position: list):
        x_smoothed = self.prev_mouse_location[0] + self.smoothing_factor * (target_position[0] - self.prev_mouse_location[0])
        y_smoothed = self.prev_mouse_location[1] + self.smoothing_factor * (target_position[1] - self.prev_mouse_location[1])
        self.prev_mouse_location = [x_smoothed, y_smoothed]

        return [x_smoothed, y_smoothed]

    def move_mouse(self, camera_width: int, camera_height: int):
        if self.set_moving_mode(self):
            print("true")
            target_position = self.change_coordinates(self, camera_width=camera_width, camera_height=camera_height)
            smooth_position = self.smoothening_mouse_move(self = self, target_position=target_position)
            pyautogui.moveTo(smooth_position[0], smooth_position[1])

    def stimulate_mouse_left_click(self, image: cv2.Mat):
        if self.set_left_click_mode(self):
            distance = self.find_distance(self)
            if distance < self.click_threshold:
                cv2.circle(image, (self.index_finger[0], self.index_finger[1]),
                           15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()
        return image

    def stimulate_mouse_right_click(self, image: cv2.Mat):
        if self.set_right_click_mode(self):
            distance = self.find_distance(self)
            if distance < self.click_threshold:
                cv2.circle(image, (self.middle_finger[0], self.middle_finger[1]),
                           15, (0, 255, 0), cv2.FILLED)
                pyautogui.rightClick()
        return image


def main():
    camera_width, camera_height = 1280, 640
    camera = cv2.VideoCapture(0)
    camera_settings(camera=camera, camera_width=camera_width, camera_height=camera_height)
    previous_time = 0
    current_mouse_position = pyautogui.position()
    hand_detector = htm.HandIdentifier(maxHands=1)
    virtual_mouse = VirtualMouse(hand_detector=hand_detector,
                                 initial_mouse_location=[current_mouse_position.x, current_mouse_position.y],
                                 click_threshold=50)

    while True:
        capture_succeed, image = camera.read()
        image = cv2.flip(image, 1)

        image, previous_time = display_fps(image=image,previous_time=previous_time)
        image = virtual_mouse.get_landmarks(image=image)
        virtual_mouse.get_index_and_middle_finger()
        virtual_mouse.detect_fingers_Up()
        virtual_mouse.move_mouse(camera_width=camera_width, camera_height=camera_height)
        image = virtual_mouse.stimulate_mouse_left_click(image=image)
        image = virtual_mouse.stimulate_mouse_right_click(image=image)

        cv2.imshow("virtual mouse", image)
        # press esc to quit
        if cv2.waitKey(1) & 0xFF == 27:
            break


if __name__ == "__main__":
    main()



