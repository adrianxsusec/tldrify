import sys
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

text = sys.argv[1]

model_name = "rishivijayvargiya/outputs-project-id2223"
tokenizer = AutoTokenizer.from_pretrained(model_name, legacy=False, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

inputs = tokenizer(text, return_tensors="pt")
outputs = model.generate(
    **inputs,
    max_new_tokens=100,
    num_beams=4,
    early_stopping=True
)
result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(result)