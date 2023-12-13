import cv2
import numpy as np

global cam_w, cam_h, hand_state, hand_x, hand_y, pre_image, post_image


def initialize(cam):
    global cam_w, cam_h, hand_state, hand_x, hand_y, pre_image, post_image
    cam_w = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    cam_h = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    hand_state = None
    hand_x = cam_w / 2
    hand_y = cam_h / 2
    pre_image = np.zeros((cam_h, cam_w, 3), np.uint8)
    post_image = np.zeros((cam_h, cam_w, 3), np.uint8)
