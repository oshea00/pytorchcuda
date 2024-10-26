from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1',
    # required but ignored
    api_key='ollama'
)

def answer_question(question):
  completion = client.chat.completions.create(
    model="llama3.1:latest",
    messages=[{"role":"user","content":question}],
    extra_headers={"X_CUST":"Mike"},
    temperature=0,
    top_p=1,
    max_tokens=1500,
    stream=True
  )

  return completion

# take a prompt from the console process with answer_question.
# if the question is "exit", break the loop
while True:
  try:
    question = input("Ask a question ('exit' to quit): ")
    if question == "exit":
      break
    completion = answer_question(question)
    for chunk in completion:
      if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end='')
    print()
  except Exception as e:
    print()
    break    
