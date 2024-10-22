import os
import cv2
import numpy as np
import face_recognition


def load_images(path: str):
    result = []
    file_path = os.listdir(path)
    for file in file_path:
        full_path = path + '/' + file
        print(full_path)
        image = face_recognition.load_image_file(file=full_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # 统一设置图片大小
        image = cv2.resize(image, (640, 480))
        result.append(image)
    return result


class ImageRecognizer:
    def __init__(self, sample_image: list, test_image: list):
        self.sample_image = sample_image
        self.test_image = test_image
        self.sample_encoding_list = self.encode_images(self.sample_image)
        self.test_encoding_list = self.encode_images(self.test_image)

    @staticmethod
    def encode_images(image_list):
        encoding_list = []
        for image in image_list:
            encoding = face_recognition.face_encodings(face_image=image)[0]
            encoding_list.append(encoding)
        print(f'length of the encoding list is {len(encoding_list)}')
        return encoding_list

    def find_distance(self):
        best_match_index = []
        for test in self.test_encoding_list:
            distance = face_recognition.face_distance(self.sample_encoding_list, test)
            index = np.argmin(distance)
            print(f"best match in database is No.{index} image")
            best_match_index.append(index)
        return best_match_index



def main():
    sample_list = load_images("samples")
    test_list = load_images("test_image")

    face_identifier = ImageRecognizer(sample_list, test_list)
    best_match = face_identifier.find_distance()

    while True:
        index = 1
        for match in best_match:
            cv2.imshow(f"best match for test case {index}",sample_list[match])
            cv2.imshow(f"test case {index}", test_list[index-1])
            index += 1
        if cv2.waitKey(1) & 0xFF == 27:
            break


if __name__ == "__main__":
    main()
