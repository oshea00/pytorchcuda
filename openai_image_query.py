from openai import OpenAI
import base64


apikey = "<enter>"
client = OpenAI(base_url="https://openai.api.x.ai/v1/", api_key=apikey)
# client = OpenAI(api_key=apikey)


def encode_image_to_base64(image_path):
    """
    Encode an image file to base64 string
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def ask_gpt4o_about_image(image_path, prompt="What are the words in this image?"):
    """
    Send an image to GPT-4o and ask a question about it
    """
    # For a local file: encode to base64
    base64_image = encode_image_to_base64(image_path)

    # Create the API request
    response = client.chat.completions.create(
        model="gpt-4o",  # Specify GPT-4o model
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high",  # Request high detail analysis
                        },
                    },
                ],
            }
        ],
    )

    # Return the model's response
    return response.choices[0].message.content


# Example usage
image_path = "awscourses.jpg"  # Replace with your image path
result = ask_gpt4o_about_image(image_path)
print(result)
