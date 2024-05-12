import requests
import json
import os

HF_TOKEN = os.getenv("HF_TOKEN")

# url from https://ui.endpoints.huggingface.co/oshea00/endpoints
url = "https://u4v1bxj4ljtel4dq.us-east-1.aws.endpoints.huggingface.cloud"
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {HF_TOKEN}'
}
data = {
    "inputs": "Deploying my first endpoint was an amazing experience."
}

response = requests.post(url, headers=headers, data=json.dumps(data))

# print the response (if you want to see it)
print(response.json())