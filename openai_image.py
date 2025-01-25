import os
from dotenv import load_dotenv
from openai import OpenAI
import base64

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# print(api_key)

client = OpenAI()

# read image file and convert to base64
# Path to your image
image_path = "graph1.png"

# with open("graph1.png", "rb") as image_file:
#     image_base64 = base64.b64encode(
#         image_file.read()
#     ).decode("utf-8")


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


# Getting the Base64 string
base64_image = encode_image(image_path)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is in this image?",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                },
            ],
        }
    ],
)

print(response.choices[0].message.content)
