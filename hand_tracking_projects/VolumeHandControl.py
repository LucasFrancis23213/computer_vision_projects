import cv2
import time
import numpy as np
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import HandTrackingMain


# 使用大拇指和食指调整音量大小

def camera_settings(camera, screen_width: int = 1280, screen_height: int = 720):
    camera.set(3, screen_width)
    camera.set(4, screen_height)


def display_fps(image, previous_time):

    current_time = time.time()
    fps = 1 / (current_time - previous_time)

    # 将当前的fps呈现出来
    cv2.putText(image, f'press "esc" to quit current fps is {int(fps)}', (40, 70),
                cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
    return image, current_time



class VolumeHandControl:

    def __init__(self, hand_detector: HandTrackingMain.HandIdentifier, volume):
        self.hand_detector = hand_detector
        self.landmark_list = []
        self.thumb_position = []
        self.index_finger_position = []
        self.volume = volume
        self.maxVolume = 0
        self.minVolume = 0

    def initialize(self, image):
        image = self.hand_detector.findHands(image=image)
        self.landmark_list = self.hand_detector.findPosition(image=image, draw=False)
        self.minVolume = self.volume.GetVolumeRange()[0]
        self.maxVolume = self.volume.GetVolumeRange()[1]
        return image

    def find_thumb_and_index_finger_position(self, image, draw: bool = True):
        thumb_position, index_finger_position = [], []
        if len(self.landmark_list) != 0:
            self.thumb_position = [self.landmark_list[4][1], self.landmark_list[4][2]]
            self.index_finger_position = [self.landmark_list[8][1], self.landmark_list[8][2]]
            if draw:
                cv2.circle(image, (self.thumb_position[0], self.thumb_position[1]), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(image, (self.index_finger_position[0], self.index_finger_position[1]), 15, (255, 0, 255), cv2.FILLED)
                cv2.line(image, self.thumb_position, self.index_finger_position, (255, 0, 255), 3)
        return self.thumb_position, self.index_finger_position

    def calculate_length(self):
        """
        计算大拇指和食指之间的距离
        手指长度的范围是20-200
        声音范围为-65-0
        """
        if len(self.index_finger_position) > 0 and len(self.thumb_position) > 0:
            x = self.index_finger_position[0] - self.thumb_position[0]
            y = self.index_finger_position[1] - self.thumb_position[1]
            length = math.hypot(x, y)
            print(f'thumb and index finger range is {length}')
            return length

    def convert_length_to_volume(self, image, display_bar:bool=True):
        length = self.calculate_length()
        if length is not None:
            vol = np.interp(length, [20,200], [self.minVolume, self.maxVolume])
            vol_bar = 400
            self.volume.SetMasterVolumeLevel(vol, None)
            if display_bar:
                vol_bar = np.interp(length, [20,200], [400, 150])
                vol_percentage = np.interp(length, [20,200], [0,100])
                cv2.rectangle(image,(50,150), (85, 400), (0,255,0),3)
                cv2.rectangle(image, (50, int(vol_bar)), (85, 400), (255, 0, 0), cv2.FILLED)
                cv2.putText(image, f'current volume percentage is {int(vol_percentage)}', (40, 450),
                            cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        return image

def main():
    # 设置窗口大小
    camera = cv2.VideoCapture(0)
    camera_settings(camera=camera, screen_width=640, screen_height=480)
    previous_time = 0
    # 设置控制电脑音频变化的变量
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    # 初始化volume controller
    hand_detector = HandTrackingMain.HandIdentifier(detectionCon=0.7)
    volume_controller = VolumeHandControl(hand_detector=hand_detector, volume=volume)

    while True:

        camera_read_succeed, image = camera.read()
        if not camera_read_succeed:
            print("摄像头未正常工作")
            break

        image = volume_controller.initialize(image)
        volume_controller.find_thumb_and_index_finger_position(image=image)
        volume_controller.calculate_length()
        image = volume_controller.convert_length_to_volume(image=image)

        image, previous_time = display_fps(image, previous_time)
        cv2.imshow("volume hand control", image)
        # 按q键退出
        if cv2.waitKey(1) & 0xFF == 27:
            break


if __name__ == '__main__':
    main()
