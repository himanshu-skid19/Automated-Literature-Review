import json
import requests
import base64

def run_llava(image_path):
    with open(image_path, "rb") as image_file:
     image_base = base64.b64encode(image_file.read()).decode('utf-8')

    url = "http://localhost:11434/api/generate"

    payload = {
    "model": "llava",
    "prompt": "identify any tables from this image and extract the data from it and structure your output in the form of a json object. It should have a caption starting with 'Table'", 
    "stream": False, 
    "images": [image_base]
    }

        
    response = requests.post(url, data = json.dumps(payload))

    return response
