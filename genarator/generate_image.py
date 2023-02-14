import requests
import json

QUERY_URL = "https://api.openai.com/v1/images/generations"

def generate_image(prompt, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    model = "image-alpha-001"
    data = {
        "model": model,
        "prompt": prompt,
        "num_images":1,
        "size":"1024x1024"
    }

    resp = requests.post(QUERY_URL, headers=headers, data=json.dumps(data))

    if resp.status_code != 200:
        raise ValueError("Failed to generate image")

    response_text = json.loads(resp.text)
    path = "image.png"
    if response_text['data'][0]['url']:
        image_url = response_text['data'][0]['url']
        response = requests.get(image_url)
        with open(path, "wb") as f:
            f.write(response.content)
        return path
    return None