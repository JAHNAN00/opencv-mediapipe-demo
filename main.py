# By John Zhang
# A simple opencv mediapipe demo

import cv2
import mediapipe as mp
import numpy as np
from src.beep import beep
from src.warn import warn_start,warn_change


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

    # 启动警告页面
    warn_start()

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

        # 变量
        hull_index = [0, 1, 2, 3, 6, 10, 14, 19, 18, 17, 10]
        hand = {
            "Left": {
                "exist": False,
                "points": list(),
                "hull": None
            },
            "Right": {
                "exist": False,
                "points": list(),
                "hull": None
            }
        }

        # 识别手部
        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                # 获取手的边别信息
                hand_side = handedness.classification[0].label
                hand[hand_side]["exist"] = True
                list_lms = []
                for i in range(21):
                    pos_x = hand_landmarks.landmark[i].x * image_width
                    pos_y = hand_landmarks.landmark[i].y * image_height
                    list_lms.append([int(pos_x), int(pos_y)])
                list_lms = np.array(list_lms, dtype=np.int32)
                hand[hand_side]["points"] = list_lms
                hand[hand_side]["hull"] = cv2.convexHull(
                    list_lms[hull_index, :])

                # 绘制手部关键点和连线。
                mp_drawing.draw_landmarks(image, hand_landmarks,
                                          mp_hands.HAND_CONNECTIONS)
                cv2.polylines(image, [hand[hand_side]["hull"]], True,
                              (0, 255, 0), 2)

        # 识别手势
        fingers_index = [4,8,12,16,20] #拇指，食指，中指，无名指，小指
        
        out_fingers=dict()
        for hand_side in ["Left","Right"]:
            out_fingers[hand_side]=list()
            for i in fingers_index:
                if hand[hand_side]["exist"]:
                    pt = (int(hand[hand_side]["points"][i][0]), int(hand[hand_side]["points"][i][1]))
                    dist = cv2.pointPolygonTest(hand[hand_side]["hull"], pt, True)
                    if dist < 0:
                        out_fingers[hand_side].append(i)
        
        #执行动作
        if out_fingers["Left"]==[4,8,20] and out_fingers["Right"]==[4,8,20]:
            #左手举1 2，右手蜘蛛侠
            beep()
        if out_fingers["Right"]==[4,8]:
            #右手
            warn_change(1)
        else:
            warn_change(0)
        # up_fingers = []
        # for i in fingers_index:
        #     if hand["Right"]["exist"]:
        #         pt = (int(hand["Right"]["points"][i][0]), int(hand["Right"]["points"][i][1]))
        #         dist = cv2.pointPolygonTest(hand["Right"]["hull"], pt, True)
        #         if dist < 0:
        #             up_fingers.append(i)
        # print(up_fingers)

        # 显示结果。
        cv2.imshow('Hand Tracking', image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    # 释放资源并关闭窗口。
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
