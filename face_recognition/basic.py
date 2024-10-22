import os
import cv2
import numpy as np
import face_recognition


def load_image(path: str):
    # 加载图片并将其转化为RGB图像
    image = face_recognition.load_image_file(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def find_face(image, draw: bool = True):
    # 找到原始照片中人脸的相对位置以及人脸的128个特征值
    face_location = face_recognition.face_locations(img=image)[0]
    face_encoding = face_recognition.face_encodings(face_image=image)[0]
    print(f'face location is {face_location}, and face encoding is {face_encoding}')
    if draw:
        cv2.rectangle(image, (face_location[3], face_location[0]), (face_location[1], face_location[2]),
                      color=(255, 0, 255), thickness=2)
    return face_location, face_encoding


def find_face_distance(known_face_encoding: list, test_case_encoding):
    result = face_recognition.face_distance(known_face_encoding, test_case_encoding)
    print(f'face difference is {result}')
    return result


def compare_face(known_face_encoding: list, test_case_encoding):
    result = face_recognition.compare_faces(known_face_encoding, test_case_encoding)
    print(f'face match result is {result}')
    return result


def main():
    train_img = load_image(path="samples/Elon_Mask_1.webp")
    test_img = load_image(path="samples/Jobs.jpg")

    train_loc, train_encoding = find_face(image=train_img)
    test_loc, test_encoding = find_face(image=test_img)

    compare_face(known_face_encoding=[train_encoding], test_case_encoding=test_encoding)

    while True:
        cv2.imshow("test image", test_img)
        cv2.imshow("train image", train_img)
        # cv2.imshow("test image", test_img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
