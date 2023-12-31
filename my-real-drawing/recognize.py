import cv2
import mediapipe as mp

import constants as c
import globals as g

mp_hands = mp.solutions.hands


def recognize_hand(cam_image):
    with mp_hands.Hands() as hands:
        hand_image = hands.process(cv2.cvtColor(cam_image, cv2.COLOR_BGR2RGB))
        if hand_image.multi_hand_landmarks:
            hand_landmarks = hand_image.multi_hand_landmarks[0]

            # 손가락 파악
            finger_1 = False
            finger_2 = False
            finger_3 = False
            finger_4 = False
            finger_5 = False

            dist_x = hand_landmarks.landmark[4].x - hand_landmarks.landmark[13].x
            dist_y = hand_landmarks.landmark[4].y - hand_landmarks.landmark[13].y

            if hand_landmarks.landmark[4].x < hand_landmarks.landmark[8].x or \
                    (dist_x * dist_x) + (dist_y * dist_y) > 0.01:
                finger_1 = True
            if hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y:
                finger_2 = True
            if hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y:
                finger_3 = True
            if hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y:
                finger_4 = True
            if hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y:
                finger_5 = True

            # 이전 손 상태 & 위치 저장
            g.prev_state, g.prev_x, g.prev_y = g.hand_state, g.hand_x, g.hand_y

            # 손 상태 갱신
            if finger_1 and finger_2 and finger_3 and finger_4 and finger_5:
                g.hand_state = c.State().MOVE
            elif not finger_1 and finger_2 and not finger_3 and \
                    not finger_4 and not finger_5:
                g.hand_state = c.State().DRAW
            elif not finger_1 and not finger_2 and not finger_3 and \
                    not finger_4 and not finger_5:
                g.hand_state = c.State().CLICK

            # 손 위치 갱신
            if g.hand_state == c.State().DRAW:
                g.hand_x = int(hand_landmarks.landmark[8].x * g.cam_w)
                g.hand_y = int(hand_landmarks.landmark[8].y * g.cam_h)
            else:
                g.hand_x = int(hand_landmarks.landmark[9].x * g.cam_w) - c.Pointer().SIZE // 2
                g.hand_y = int(hand_landmarks.landmark[9].y * g.cam_h) - c.Pointer().SIZE // 2

            g.hand_x = max(0, min(g.hand_x, g.cam_w - c.Pointer().SIZE))
            g.hand_y = max(0, min(g.hand_y, g.cam_h - c.Pointer().SIZE))
