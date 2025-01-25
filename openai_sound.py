import os
from dotenv import load_dotenv
from openai import OpenAI
import base64

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

mp3_path = "Recording.mp3"

from openai import OpenAI

client = OpenAI()

audio_file = open(mp3_path, "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="text",
)

print(transcription)
