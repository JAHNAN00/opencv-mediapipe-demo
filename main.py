# By John Zhang
# A simple opencv mediapipe demo

import cv2
import mediapipe as mp
import numpy as np

def main():
    # 初始化MediaPipe手部模块。
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
                        max_num_hands=2,
                        min_detection_confidence=0.5)

    # 初始化绘图功能。
    mp_drawing = mp.solutions.drawing_utils

    # 启动摄像头。
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        # 转换图像的颜色空间从BGR到RGB。
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 处理图像并检测手部。
        results = hands.process(image)

        # 将图像颜色空间转换回BGR，以便使用OpenCV显示。
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 绘制手部关键点和连线。
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # 显示结果。
        cv2.imshow('Hand Tracking', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    # 释放资源并关闭窗口。
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
