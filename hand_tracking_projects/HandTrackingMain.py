# import os
# os.chdir('D:/2024Fall/cv/Projects/hand_tracking_projects')

import cv2
import mediapipe as mp
import time


class HandIdentifier:
    def __init__(self, mode=None, maxHands: int = 2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectCon = detectionCon  # 检测置信度，默认为0.5
        self.trackCon = trackCon  # 手部追踪置信度，默认为0.5
        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(static_image_mode=self.mode,
                                       max_num_hands=self.maxHands,
                                       min_detection_confidence=self.detectCon,
                                       min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.results, self.landmarks = [], []

    def findHands(self, image, draw: bool = True):
        RGB_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image)
        # 如果检测到了手，获取并绘制手部关键点
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                # 绘制检测到的手的关键点
                if draw:
                    self.mpDraw.draw_landmarks(image, hand, self.mpHand.HAND_CONNECTIONS)
        return image

    def findPosition(self, image, hand_id=0, draw: bool = True):
        """
        默认检测第一只手
        """
        landmark_position = []
        if self.results.multi_hand_landmarks:
            # 检测哪一只手
            target_hand = self.results.multi_hand_landmarks[hand_id]
            for landmark_id, landmark in enumerate(target_hand.landmark):
                # 这里将一只手的关键点全部找到
                # mediapipe给手找到了21个特征点以描述它(这里只找一个)
                # landmark其实就是手上出现的那些点的三维坐标
                height, width, channel = image.shape
                center_x, center_y = int(landmark.x * width), int(landmark.y * height)
                # print(f'id = {landmark_id}, center:({center_x},{center_y})')
                landmark_position.append([landmark_id, center_x, center_y])
                if draw:
                    cv2.circle(img=image, center=(center_x, center_y),
                               radius=10, color=(255, 0, 0), thickness=cv2.FILLED)
        self.landmarks = landmark_position
        return landmark_position




def main():
    previous_time = 0
    current_time = 0

    # 初始化摄像头
    # 电脑只有一个摄像头所以索引值为0
    camera = cv2.VideoCapture(0)
    detector = HandIdentifier()

    while True:
        read_successful, image = camera.read()
        if not read_successful:
            print('unable to read image')
            break

        image = detector.findHands(image)
        target_landmark = detector.findPosition(image)
        if len(target_landmark) != 0:
            print(target_landmark[4])

        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time

        cv2.putText(image, f"press 'esc' to quit, current fps is {str(int(fps))}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
        cv2.imshow("test running", image)

        # 按esc键退出
        if cv2.waitKey(1) & 0xFF == 27:
            break

if __name__ == '__main__':
    main()
