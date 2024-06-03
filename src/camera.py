import cv2
import mediapipe as mp


class camera:

    def __init__(self):
        # 初始化 MediaPipe 手部模块。
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,  # 非静态图像模式
            max_num_hands=2,  # 最多检测两只手
            min_detection_confidence=0.5,  # 检测置信度阈值
            min_tracking_confidence=0.5)  # 跟踪置信度阈值
        self.mp_drawing = mp.solutions.drawing_utils  # 绘图辅助工工具
        self.cap = cv2.VideoCapture(0)  # 捕获视频

    def shot(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("无法读取摄像头画面，退出...")

            # 将图像从 BGR 转换到 RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            # 将图像从 RGB 转回 BGR 以显示
            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

            # 绘制手部标记
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame_bgr,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing.DrawingSpec(color=(121, 22, 76),
                                                    thickness=2,
                                                    circle_radius=4),
                        self.mp_drawing.DrawingSpec(color=(250, 44, 250),
                                                    thickness=2,
                                                    circle_radius=2),
                    )

            # 显示图像
            cv2.imshow('MediaPipe Hands', frame_bgr)
            if cv2.waitKey(5) & 0xFF == 27:  # 按 'ESC' 键退出
                return

    def close(self):
        # 释放资源
        self.cap.release()
        cv2.destroyAllWindows()
