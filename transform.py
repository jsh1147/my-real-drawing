import base64
import os
import requests

api_key = os.getenv("STABILITY_API_KEY")
api_host = os.getenv("API_HOST", "https://api.stability.ai")
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
        # 사진 파일 열기
        "init_image": open("baby1.png", "rb")
    },
    data={
        "image_strength": 0.35,
        "init_image_mode": "IMAGE_STRENGTH",
        # 프롬포트 작성
        "text_prompts[0][text]": "In the style of a master artist, express it in a high quality artistic painting. And draw the background naturally to match the painting. If there is no background in the painting, color it in harmony with the painting",
        # 가이던스 스케일 (cfg_scale): 프롬프트 텍스트에 얼마나 엄격하게 따를 것인지 정의합니다.
        "cfg_scale": 35,
        # 출력 이미지 수 (samples): 생성할 이미지의 수입니다.
        "samples": 1,
        # 스텝 수 (steps): 확산 과정에서 사용할 스텝의 수입니다.
        "steps": 30,
    }
)

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

data = response.json()

for i, image in enumerate(data["artifacts"]):
    file_path = f"v1_img2img_{i}.png"
    with open(file_path, "wb") as f:
        f.write(base64.b64decode(image["base64"]))