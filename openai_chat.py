from openai import OpenAI
import os
import json  # Add this import

apikey = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=apikey)

# create a multi-line prompt
prompt = """
Hello chatgpt, are you ready to work? Can you describe general relativity?
"""

#MODEL = "gpt-4.5-preview"
MODEL = "gpt-4o"

completion = client.chat.completions.create(
  model=MODEL,
  messages=[{"role":"user","content":f"{prompt}"}],
  temperature=0,
  stream=True
)

# Serialize the completion object to JSON
# completion_json = completion.model_dump_json(indent=2)
# print(completion_json)

for chunk in completion:
  if chunk.choices and chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")

# print(completion.choices[0].message.content)
