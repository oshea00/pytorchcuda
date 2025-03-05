from openai import OpenAI
import base64


apikey = "eyJraWQiOiI3RVljV2sxX1UyWXdWWTh4Y19feDFWQ3hhR3dWMlVyRDYxMGhrZWh2amZjIiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULi04UEM1NXhHMEcxUERLSGs1TXUzN21yLURTSlN1R1psM05qVWJoeGtIWDAiLCJpc3MiOiJodHRwczovL2VhdG9udmFuY2VkZXYub2t0YXByZXZpZXcuY29tL29hdXRoMi9hdXMyOHMxaDh0NTk5NXMzajBoOCIsImF1ZCI6InJhZGl1c2FpLXNlcnZpY2UiLCJpYXQiOjE3NDExNDA4MjQsImV4cCI6MTc0MTE0NDQyNCwiY2lkIjoiMG9hMmMxYmxvYXNwb0JQdE4waDgiLCJ1aWQiOiIwMHVyaHJmMGQ0MXdNME1iZTBoNyIsInNjcCI6WyJSQURJVVNBSV9DT01QTEVUSU9OIl0sImF1dGhfdGltZSI6MTc0MTE0MDgyMiwic3ViIjoiTWljaGFlbE9AcGFyYXBvcnQuY29tIn0.KufkGpG58EfdrFRgePyadgugUM865vfCeuPmf3EpvW28QAaoYF4bXKDEmwlgwHpAllwXN1ZqUQBff_X735WF-VMmJJnScKgrtgeBONSHzxC3DZF21SUdkFYaZkSrv8k9ZrmPTJQek-OrETvjvSGs3l5Tr48AA_jgonDj8Im6ytAx6g1HqnJ8tOzoMPsnJiPd3O4ldsoyOSRwNekDFtvMC1CFje3J3eCUeTe81LopvvQYp30bMaNLHGbfWWF-jBJ0_8YmvIDZQ7O1wZvyQlDNd4KzMU8HHcvmymRtRNIBwRa3XvgY6rxH8-Bz1nUNdvs7oWGB_6hr4i2bg8cupcZ4sA"
client = OpenAI(
#    base_url="https://api-uat.morganstanley.com/wm-aidp/aigateway/v1/openai/v1",
    base_url="https://radai-dev.sandbox.genai.use1.aws.paraport.com/v1",
    api_key=apikey
)

def encode_image_to_base64(image_path):
    """
    Encode an image file to base64 string
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

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
                            "detail": "high"  # Request high detail analysis
                        }
                    }
                ]
            }
        ]
    )

    # Return the model's response
    return response.choices[0].message.content

# Example usage
image_path = "graph2.png"  # Replace with your image path
result = ask_gpt4o_about_image(image_path)
print(result)

