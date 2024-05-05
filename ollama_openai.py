from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1',
    # required but ignored
    api_key='ollama'
)

completion = client.chat.completions.create(
  model="llama3",
  messages=[{"role":"user","content":"What can I see at NVIDIA's GPU Technology Conference?"}],
  temperature=0.5,
  top_p=1,
  max_tokens=1024,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")
