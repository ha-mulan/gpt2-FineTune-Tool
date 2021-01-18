from transformers import AutoModelWithLMHead, AutoTokenizer, top_k_top_p_filtering
import torch
from flask import Flask, request, Response, jsonify
from torch.nn import functional as F
from queue import Queue, Empty
import time
import threading
import re
import json
# from sklearn.model_selection import train_test_split



from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2-large")

train_path = './test.txt'
test_path = './test.txt'
#train_path = '/home/workspace/gpt2-fine-tuning/test.txt'
#test_path = '/home/workspace/gpt2-fine-tuning/test.txt'

from transformers import TextDataset,DataCollatorForLanguageModeling

def load_dataset(train_path,test_path,tokenizer):
    train_dataset = TextDataset(
          tokenizer=tokenizer,
          file_path=train_path,
          block_size=128)

    test_dataset = TextDataset(
          tokenizer=tokenizer,
          file_path=test_path,
          block_size=128)

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )
    return train_dataset,test_dataset,data_collator

train_dataset,test_dataset,data_collator = load_dataset(train_path,test_path,tokenizer)
from transformers import Trainer, TrainingArguments,AutoModelWithLMHead

model = AutoModelWithLMHead.from_pretrained("gpt2-large")


training_args = TrainingArguments(
    output_dir="./result", #The output directory
    overwrite_output_dir=True, #overwrite the content of the output directory
    num_train_epochs=3, # number of training epochs
    per_device_train_batch_size=16, # batch size for training
    per_device_eval_batch_size=32,  # batch size for evaluation
    eval_steps = 400, # Number of update steps between two evaluations.
    save_steps=800, # after # steps model is saved
    warmup_steps=500,# number of warmup steps for learning rate scheduler
    )


trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
    # prediction_loss_only=True,
)
trainer.train("result")
trainer.save_model("result")
tokenizer.save_pretrained("result")
