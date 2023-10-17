import cv2
import mediapipe as mp
import numpy as np
import os
from PIL import Image
from ultralytics import YOLO

model = YOLO('best.pt')

class DetectImageFinger:

    def __init__(self, image_paths):
        self.IMAGE_FILES = image_paths
        self.mp_hands = mp.solutions.hands
        # YOLO 모델을 초기화
        self.model = model

    def process_images(self):
        results_list = []

        for image_file_path in self.IMAGE_FILES:
            image = self.load_and_preprocess_image(image_file_path)
            if image is None:
                continue
            else:
                image = cv2.flip(image, 1)

            results = self.detect_hand_landmarks(image)

            if not results.multi_hand_landmarks:
                result = "safe"
            else: 
                model_result = self.process_hand_landmarks(results.multi_hand_landmarks[0], image)
                if model_result:
                    result = "danger"
                else:
                    result = "safe"

            results_list.append((result, image))

        return results_list
    
    def process_hand_landmarks(self, hand_landmarks, image):
        landmark_4 = hand_landmarks.landmark[4] 
        landmark_8 = hand_landmarks.landmark[8]
        landmark_12 = hand_landmarks.landmark[12]
        landmark_16 = hand_landmarks.landmark[16]
        landmark_20 = hand_landmarks.landmark[20]
        image_height, image_width, _ = image.shape
        model_result = False

        for i in range(4, 21, 4):
            for landmark in [landmark_4, landmark_8, landmark_12, landmark_16, landmark_20]:
                x_px = hand_landmarks.landmark[i].x * image_width
                y_px = hand_landmarks.landmark[i].y * image_height
                annotated_image = image[int(y_px) - 20:int(y_px) + 20, int(x_px) - 20:int(x_px) + 20]
                detections = self.run_model_on_annotated_image(annotated_image)

                for det in detections:
                    if int(det[5]) == 2:
                        image = self.blur_detected_region(image, x_px, y_px)
                        model_result = True

        return model_result

    # 이미지 파일 불러오기
    def load_and_preprocess_image(self, image_file_path):
        try:
            image = Image.open(image_file_path)
            image = np.array(image)  # 이미지를 NumPy 배열로 변환
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # BGR로 변환
            return image
        except Exception as e:
            print(f"Error: Unable to read image from {image_file_path}: {e}")
            return None
        
    # 손 끝 인식 초기화
    def detect_hand_landmarks(self, image):
        with self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=2,
            min_detection_confidence=0.5) as hands:
            return hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
    # 모델 적용
    def run_model_on_annotated_image(self, annotated_image):
        results = model(annotated_image, augment=True)
        tensor_list = results[0].boxes.data
        return tensor_list.tolist()
    
     # 자른 이미지 blur 처리
    def blur_detected_region(self, image, x_px, y_px):
        # 자른 이미지를 Gaussian Blur로 처리
        image_height, image_width, _ = image.shape
        blur_radius = 20
        x_px = int(x_px)
        y_px = int(y_px)

        x_start = max(0, x_px - blur_radius)
        x_end = min(image_width, x_px + blur_radius)
        y_start = max(0, y_px - blur_radius)
        y_end = min(image_height, y_px + blur_radius)

        roi = image[y_start:y_end, x_start:x_end]
        blurred_roi = cv2.GaussianBlur(roi, (0, 0), sigmaX=1, sigmaY=1)
        image[y_start:y_end, x_start:x_end] = blurred_roi

        return image

    # blur 처리 이미지 적용하기
    def save_blurred_image(self, image, file_name):
        cv2.imwrite(file_name, image)
        return file_name

# 이미지 파일 경로를 가져오는 부분 수정
image_file_paths = []

# 불러올 디렉토리 경로
directory_path = 'media'

# 디렉토리 내의 이미지 파일 경로 목록 가져오기
for file_name in os.listdir(directory_path):
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        file_path = os.path.join(directory_path, file_name)
        image_file_paths.append(file_path)