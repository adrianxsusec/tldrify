import sys
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

text = sys.argv[1]

model_name = "rishivijayvargiya/outputs-project-id2223"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

inputs = tokenizer(text, return_tensors="pt")
outputs = model.generate(**inputs)
print(tokenizer.decode(outputs[0]))