from transformers import pipeline

# Use a pipeline as a high-level helper
# pipeline will look for HF_TOKEN env variable
# to authenticate with Hugging Face.
pipe = pipeline("text-generation", model="meta-llama/Meta-Llama-3-8B", device=0)
output = pipe("Hey how are you doing today?")
print(output[0]['generated_text'])
