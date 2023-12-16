import cv2
import numpy as np

import constants as c
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
    if g.prev_state == c.State().DRAW:
        cv2.line(g.pre_image, (g.prev_x, g.prev_y), (g.hand_x, g.hand_y), g.color, 8)
    else:
        cv2.circle(g.pre_image, (g.hand_x+4, g.hand_y+4), 4, g.color, -1)


def draw_pre_image(img):
    draw_masked(img, g.pre_image, 0, 0)


def draw_button(img):
    cb = c.Button()

    # 색상 버튼
    color_x = g.cam_w - (cb.COLOR_WIDTH + cb.COLOR_GAP + cb.ETC_WIDTH + cb.ETC_GAP)
    color_y = 0 + cb.ETC_GAP
    for i in range(len(cb.COLOR_VALUE)):
        button = np.full((cb.COLOR_HEIGHT, cb.COLOR_WIDTH, 3), cb.COLOR_VALUE[i], np.uint8)
        cv2.rectangle(button, (0, 0), (cb.COLOR_WIDTH, cb.COLOR_HEIGHT), (0, 0, 0), 4)
        draw_non_masked(img, button, color_x, color_y + (i * (cb.COLOR_HEIGHT + cb.COLOR_GAP)))

    # 기타 버튼(지우개, 초기화, 변환, 저장, 종료)
    etc_x = g.cam_w - (cb.ETC_WIDTH + cb.ETC_GAP)
    etc_y = 0 + cb.ETC_GAP
    for i in range(len(cb.ETC_VALUE)):
        button = np.full((cb.ETC_HEIGHT, cb.ETC_WIDTH, 3), (255, 255, 255), np.uint8)
        cv2.rectangle(button, (0, 0), (cb.ETC_WIDTH, cb.ETC_HEIGHT), (0, 0, 0), 4)
        text_size = cv2.getTextSize(cb.ETC_VALUE[i], cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        cv2.putText(button, cb.ETC_VALUE[i],
                    ((cb.ETC_WIDTH - text_size[0]) // 2 + 4, (cb.ETC_HEIGHT + text_size[1]) // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        draw_non_masked(img, button, etc_x, etc_y + (i * (cb.ETC_HEIGHT + cb.ETC_GAP)))


def draw_pointer(img):
    pointer = cv2.imread(f"./assets/{g.hand_state}.png", cv2.IMREAD_UNCHANGED)
    draw_masked(img, pointer, g.hand_x, g.hand_y)


def draw_gui(img):
    draw_pre_image(img)
    draw_button(img)
    draw_pointer(img)
