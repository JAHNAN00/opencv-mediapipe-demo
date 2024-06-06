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
        # 水平翻转图像，以便左右手正确显示
        image = cv2.flip(image, 1)

        #储存长宽
        image_height, image_width, _ = np.shape(image)

        # 处理图像并检测手部。
        results = hands.process(image)

        # 将图像颜色空间转换回BGR，以便使用OpenCV显示。
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        #凸包
        hull_index = [0, 1, 2, 3, 6, 10, 14, 19, 18, 17, 10]

        #记录左右手的手势
        left_ges=None
        right_ges=None

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # 绘制手部关键点和连线。
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                # 获取手的边别信息
                hand_side = handedness.classification[0].label
                if hand_side=="Left":
                    # 采集所有关键点的坐标
                    hand=hand_landmarks
                    list_lms = []
                    for i in range(21):
                        pos_x = hand.landmark[i].x * image_width
                        pos_y = hand.landmark[i].y * image_height
                        list_lms.append([int(pos_x), int(pos_y)])
                    list_lms = np.array(list_lms, dtype=np.int32)
                    
                    hull = cv2.convexHull(list_lms[hull_index, :])
                    cv2.polylines(image, [hull], True, (0, 255, 0), 2)

                    #print("left")
                    pass

                elif hand_side=="Right":
                    #print("right")
                    pass

        # 显示结果。
        cv2.imshow('Hand Tracking', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    # 释放资源并关闭窗口。
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
