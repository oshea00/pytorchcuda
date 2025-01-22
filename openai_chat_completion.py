from openai import OpenAI
import os

# BASE_URL = "https://api.x.ai/v1/"
# API_KEY = os.getenv("XAI_API_KEY")
# MODEL = "grok-beta"

BASE_URL = "http://localhost:1234/v1/"
API_KEY = "na"
MODEL = "llama-3.2-1b-instruct"

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

# system prompt
system_prompt = """
You are a helpful AI assistant who speaks like Montgomery Scott.
"""

# create a multi-line prompt
prompt = """
say hello and introduce yourself, then explain how a warp drive might be the size of an egg.
"""

completion = client.chat.completions.create(
  model=MODEL,
  messages=[
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": prompt}
  ],
  temperature=0.5,
  top_p=1,
  # max_tokens=4096,
  stream=False
)

# get result and print to console
result = completion.choices[0].message.content
print(result)