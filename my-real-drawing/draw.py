import cv2
import numpy as np

import globals as g


def draw_non_masked(base_img, added_img, x, y):
    h, w = added_img.shape[:2]
    base_img[y:y+h, x:x+w] = added_img


def draw_masked(base_img, added_img, x, y):
    h, w = added_img.shape[:2]

    _, mask = cv2.threshold(added_img[:, :, 3], 1, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    added_img = cv2.cvtColor(added_img, cv2.COLOR_BGRA2BGR)
    roi = base_img[y:y + h, x:x + w]

    masked_fg = cv2.bitwise_and(added_img, added_img, mask=mask)
    masked_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    added = masked_fg + masked_bg
    base_img[y:y + h, x:x + w] = added


def draw_dot():
    if g.prev_state == 'pointing':
        cv2.line(g.pre_image, (g.prev_x, g.prev_y), (g.hand_x, g.hand_y), g.color, 8)
    else:
        cv2.circle(g.pre_image, (g.hand_x+4, g.hand_y+4), 4, g.color, -1)


def draw_pre_image(img):
    draw_masked(img, g.pre_image, 0, 0)


def draw_button(img):
    button = np.zeros((64, 256, 3), np.uint8)
    cv2.rectangle(button, (00, 00), (256, 64), (255, 255, 255), 4)
    draw_non_masked(img, button, 16, 16)


def draw_pointer(img):
    pointer = cv2.imread(f"./assets/{g.hand_state}.png", cv2.IMREAD_UNCHANGED)
    draw_masked(img, pointer, g.hand_x, g.hand_y)


def draw_gui(img):
    draw_pre_image(img)
    draw_button(img)
    draw_pointer(img)
