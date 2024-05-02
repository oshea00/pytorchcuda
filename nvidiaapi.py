from openai import OpenAI
import os

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = NVIDIA_API_KEY
)

completion = client.chat.completions.create(
  model="databricks/dbrx-instruct",
  messages=[{"role":"user","content":"What can I see at NVIDIA's GPU Technology Conference?"}],
  temperature=0.5,
  top_p=1,
  max_tokens=1024,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")


