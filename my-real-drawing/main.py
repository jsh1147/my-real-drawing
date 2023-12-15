import cv2
import numpy as np

import globals as g
import recognize as r
import transform as t
import draw as d


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
        cv2.imshow('My Real Drawing', result_image)

        # 손동작 대응
        if g.hand_state == 'draw':
            d.draw_dot()
        if g.prev_state == 'move' and g.hand_state == 'click':
            # 클릭이 발생한 손의 위치의 버튼을 동작
            t.draw_post_image()

        cv2.waitKey(1)
        if cv2.getWindowProperty('My Real Drawing', cv2.WND_PROP_VISIBLE) < 1:
            break

    # 종료 작업
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
