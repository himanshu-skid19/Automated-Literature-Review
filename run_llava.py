import json
import requests
import base64

def run_llava(prompt, image_path):
    with open(image_path, "rb") as image_file:
     image_base = base64.b64encode(image_file.read()).decode('utf-8')

    url = "http://localhost:11434/api/generate"

    payload = {
    "model": "llava",
    "prompt": prompt, 
    "stream": False, 
    "images": [image_base]
    }

        
    response = requests.post(url, data = json.dumps(payload))

    return response
