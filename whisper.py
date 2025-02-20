import requests
import os

api_key = os.getenv('OPENAI_API_KEY')
audio_file_path = '/Users/moshea/repos/pytorchcuda/audiofile.m4a'
url = 'https://api.openai.com/v1/audio/transcriptions'

with open(audio_file_path, 'rb') as audio_file:
    response = requests.post(
        url,
        headers={
            'Authorization': f'Bearer {api_key}'
        },
        files={
            'file': audio_file
        },
        data={
            'model': 'whisper-1'
        }
    )

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)
