import requests

API_URL = "https://api-inference.huggingface.co/models/microsoft/table-transformer-structure-recognition-v1.1-all"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query("pages/page_2.png")
print(output)