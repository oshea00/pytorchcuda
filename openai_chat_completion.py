from openai import OpenAI
import os

apikey = os.getenv("XAI_API_KEY")
client = OpenAI(
    base_url="https://api.x.ai/v1/",
    api_key=apikey
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
  model="grok-beta",
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