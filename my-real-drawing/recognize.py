import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


def recognize_hand(cam_image):
    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5,
                        min_tracking_confidence=0.5) as hands:
        result = hands.process(cv2.cvtColor(cam_image, cv2.COLOR_BGR2RGB))
        if result.multi_hand_landmarks:
            hand_landmarks = result.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(
                cam_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
