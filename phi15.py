import torch
import time

from transformers import AutoModelForCausalLM, AutoTokenizer

torch.set_default_device("cuda")

model = AutoModelForCausalLM.from_pretrained("microsoft/phi-1_5", torch_dtype="auto", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-1_5", trust_remote_code=True)

inputs = tokenizer('''def fizzbuzz:
   """
   print fizzbuzz algorithm recipe given number n
   """
   """''', return_tensors="pt", return_attention_mask=False)

start=time.time()
outputs = model.generate(**inputs, max_length=200)
text = tokenizer.batch_decode(outputs)[0]
end=time.time()
print(text)
print(end - start)
