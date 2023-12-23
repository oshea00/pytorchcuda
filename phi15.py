import torch
import time

from transformers import AutoModelForCausalLM, AutoTokenizer

def markTime(start,msg):
    print(f"{msg} {time.time() - start}")

start=time.time()

torch.set_default_device("cuda")

model = AutoModelForCausalLM.from_pretrained("microsoft/phi-1_5", torch_dtype="auto", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-1_5", trust_remote_code=True)
markTime(start,"load model")

inputs = tokenizer('''def fizzbuzz:
   """
   print fizzbuzz algorithm recipe given number n
   """
   """''', return_tensors="pt", return_attention_mask=False)

outputs = model.generate(**inputs, max_length=200)
markTime(start,"generate")
text = tokenizer.batch_decode(outputs)[0]
markTime(start,"decode")
print(f"Total time: {time.time() - start}")
