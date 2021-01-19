from transformers import pipeline

chef = pipeline('text-generation',model='./result', tokenizer='gpt2-large',config={'max_length':800})

print(chef("my text"))
