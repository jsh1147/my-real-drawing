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

        # 액션 반응
        action = cv2.waitKey(1)
        if action != -1:
            if action == ord('f'):
                d.draw_dot()
            elif action == ord('g'):
                t.draw_post_image()
            elif action == ord('q'):
                break
        if cv2.getWindowProperty('My Real Drawing', cv2.WND_PROP_VISIBLE) < 1:
            break

    # 종료 작업
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
