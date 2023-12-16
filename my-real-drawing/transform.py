import cv2
import base64
import os
import requests
import pyautogui
from dotenv import load_dotenv

import constants as c
import globals as g


def stable_diffusion_api(image, description):
    load_dotenv()
    api_key = os.getenv("STABILITY_API_KEY")
    api_host = "https://api.stability.ai"
    engine_id = "stable-diffusion-xl-1024-v1-0"

    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/image-to-image",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        files={
            "init_image": image
        },
        data={
            "image_strength": 0.1,
            "text_prompts[0][text]": f"{description}, (high_resolution:1.2), (distinct_image:1.2), extremely detailed CG, super detail, best illumination, High_Clarity, Intricate_Details, extremely detailed character, best Shadow",
            "text_prompts[0][weight]": 1,
            "text_prompts[1][text]": "(worst quality, low quality:1.4), (worst quality:1.2, low quality:1.2, bad anatomy:1.2, extra digit, fewer digit), text, error, signature, watermark, username, artist name, EasyNegative, (ugly, 3d realistic), (blurry:1.3), extra digit, extra arms, bad_prompt",
            "text_prompts[1][weight]": -1,
            "cfg_scale": 30,
            "steps": 40,
        }
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))
    return response.json()


def transform_image():
    cp = c.Project()
    description = pyautogui.prompt("추가적인 설명이 필요합니다.\n예) A, B, C", cp.NAME)

    transform_img = cv2.resize(g.pre_image, (1152, 896))
    cv2.imwrite(cp.TRANS_PRE_URL, transform_img)

    with open(cp.TRANS_PRE_URL, "rb") as image:
        data = stable_diffusion_api(image, description)

    for i, image in enumerate(data["artifacts"]):
        with open(cp.TRANS_POST_URL, "wb") as f:
            f.write(base64.b64decode(image["base64"]))

    transform_img = cv2.imread(cp.TRANS_POST_URL, cv2.IMREAD_COLOR)
    transform_img = cv2.resize(transform_img, (g.cam_w, g.cam_h))
    g.post_image = transform_img

    os.remove(cp.TRANS_PRE_URL)
    os.remove(cp.TRANS_POST_URL)
    g.hand_state = c.State().MOVE
