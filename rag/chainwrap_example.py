import openai
from langsmith.wrappers import wrap_openai
from langsmith import traceable

# export LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
# export LANGCHAIN_TRACING_V2=true
# export LANGCHAIN_API_KEY=ls...

# Auto-trace LLM calls in-context
client = wrap_openai(openai.Client())

@traceable # Auto-trace this function
def pipeline(user_input: str):
    result = client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}],
        model="gpt-3.5-turbo"
    )
    return result.choices[0].message.content

print(pipeline("How heavy is the sun?"))
# Out:  Hello there! How can I assist you today?