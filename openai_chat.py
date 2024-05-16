from openai import OpenAI
import os

apikey = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=apikey)

# create a multi-line prompt
prompt = """
Hello chatgpt, are you ready to work?
"""

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[{"role":"user","content":f"{prompt}"}],
  temperature=0.5,
  top_p=1,
  max_tokens=4096,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")
print()