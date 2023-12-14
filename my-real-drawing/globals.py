import cv2
import numpy as np

global cam_w, cam_h, pre_image, post_image, color, \
    hand_state, hand_x, hand_y, prev_state, prev_x, prev_y


def initialize(cam):
    global cam_w, cam_h, pre_image, post_image, color, \
        hand_state, hand_x, hand_y, prev_state, prev_x, prev_y
    cam_w = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    cam_h = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    pre_image = np.zeros((cam_h, cam_w, 4), np.uint8)
    post_image = np.zeros((cam_h, cam_w, 3), np.uint8)
    color = (255, 255, 255, 255)
    hand_state = prev_state = 'palm'
    hand_x = prev_x = int(cam_w / 2)
    hand_y = prev_y = int(cam_h / 2)
