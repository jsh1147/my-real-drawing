import cv2

import globals as g


def draw_post_image():
    cv2.rectangle(g.post_image, (0, 0), (g.cam_w, g.cam_h), (255, 255, 255), -1)
