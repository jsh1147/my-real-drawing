import cv2
import numpy as np

import constants as c
import draw as d
import globals as g
import recognize as r
import transform as t


def event_handler():
    cb = c.Button()
    etc_x = g.cam_w - (cb.ETC_WIDTH + cb.ETC_GAP)
    pointer_x = g.hand_x + c.Pointer().SIZE // 2
    pointer_y = g.hand_y + c.Pointer().SIZE // 2

    # 색상 버튼
    if etc_x - (cb.COLOR_WIDTH + cb.COLOR_GAP) <= pointer_x <= etc_x - cb.COLOR_GAP:
        g.color = cb.COLOR_VALUE[(pointer_y - cb.ETC_GAP) // (cb.COLOR_HEIGHT + cb.COLOR_GAP)] + (255,)
        g.thick = 8

    # 기타 버튼(지우개, 초기화, 변환, 저장, 종료)
    elif etc_x <= pointer_x <= etc_x + cb.ETC_WIDTH:
        target = (pointer_y - cb.ETC_GAP) // (cb.ETC_HEIGHT + cb.ETC_GAP)
        if target == 0:  # 지우개
            g.color = (0, 0, 0) + (0,)
            g.thick = 24
        elif target == 1:  # 초기화
            g.pre_image = np.zeros((g.cam_h, g.cam_w, 4), np.uint8)
        elif target == 2:  # 변환
            t.draw_post_image()
        elif target == 3:  # 저장
            cv2.imwrite(c.Project().SAVE_PRE_URL, g.pre_image)
            cv2.imwrite(c.Project().SAVE_POST_URL, g.post_image)
        elif target == 4:  # 종료
            return True
    return False


def main():
    # 초기 작업
    cam = cv2.VideoCapture(0)
    g.initialize(cam)

    # 캠 인식
    while cam.isOpened():
        success, cam_image = cam.read()
        if not success:
            continue

        # GUI 구성
        cam_image = cv2.flip(cam_image, 1)
        r.recognize_hand(cam_image)
        d.draw_gui(cam_image)
        result_image = cv2.hconcat([cam_image, g.post_image])
        cv2.imshow(c.Project().NAME, result_image)

        # 손동작 대응
        if g.hand_state == c.State().DRAW:
            d.draw_dot()
        if g.prev_state == c.State().MOVE and g.hand_state == c.State().CLICK:
            event_result = event_handler()
            if event_result:
                break

        cv2.waitKey(1)
        if cv2.getWindowProperty(c.Project().NAME, cv2.WND_PROP_VISIBLE) < 1:
            break

    # 종료 작업
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
