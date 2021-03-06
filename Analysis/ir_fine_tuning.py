# -*- coding: utf-8 -*-
"""IR_Fine_tuning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/130PJKq7KtWIOVIYVuHMYqt-La6JrccTd
"""

!pip install transformers==4.17.0
!pip install datasets==1.18.3
!pip install datasets transformers huggingface_hub
!apt-get install git-lfs

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import json
import gc
import os
import random
import pickle

import torch
from transformers import AutoModel, AutoTokenizer, AutoModelForSequenceClassification
from transformers import TrainingArguments
from transformers import Trainer
from datasets import load_metric
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, classification_report

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

from google.colab import drive
drive.mount('/content/drive')

import torch
torch.cuda.is_available()

HYPERPARAMS = {}
HYPERPARAMS["DROPOUT_PROB"] = 0.3
HYPERPARAMS["LEARNING_RATE"] = 2e-5
HYPERPARAMS["BATCH_SIZE"] = 8
HYPERPARAMS["EPOCHS"] = 4
HYPERPARAMS["RNG_SEED"] = 0
HYPERPARAMS["MAX_LEN"] = 256

folder_name = '/content/drive/MyDrive/IR_Project/Tweet Sentiment Analysis /BTC_tweets_daily_example.csv'

def load_pickle(file_name):
  with open(os.path.join(folder_name, file_name+".pkl"),"rb") as f:
    data=pickle.load(f)
  return data

df = pd.read_csv('/content/drive/MyDrive/IR_Project/Tweet Sentiment Analysis /BTC_tweets_daily_example.csv')
df = df.dropna()
df['text'] = df['Tweet']
df['label'] = df['New_Sentiment_State'] 
df_final = df[['text', 'label']]
df = df_final
# df = df[:30000]
df_train, df_test = train_test_split(df, test_size=0.3)

print(len(df_train), len(df_test))

df_train, df_val = train_test_split(df_train, test_size=0.3)

print(len(df_train), len(df_val))

df_train = df_train.reset_index()
df_train = df_train.drop(columns='index')
df_test = df_test.reset_index()
df_test = df_test.drop(columns='index')
df_val = df_val.reset_index()
df_val = df_val.drop(columns='index')

print(len(df_train), len(df_test), len(df_val))

pos_train = df_train[df_train['label']==1]
pos_train = list(pos_train['text'])

neg_train = df_train[df_train['label']==-1]
neg_train = list(neg_train['text'])

neu_train = df_train[df_train['label']==0]
neu_train = list(neu_train['text'])

print("Training : ", len(pos_train), len(neg_train), len(neu_train))

pos_test = df_test[df_test['label']==1]
pos_test = list(pos_test['text'])

neg_test = df_test[df_test['label']==-1]
neg_test = list(neg_test['text'])

neu_test = df_test[df_test['label']==0]
neu_test = list(neu_test['text'])

print("Testing : ", len(pos_test), len(neg_test), len(neu_test))

pos_val = df_val[df_val['label']==1]
pos_val = list(pos_val['text'])

neg_val = df_val[df_val['label']==-1]
neg_val = list(neg_val['text'])

neu_val = df_val[df_val['label']==0]
neu_val = list(neu_val['text'])

print("Validation : ", len(pos_val), len(neg_val), len(neu_val))

print("POS NEG NEU")
print("TRAIN", len(pos_train), len(neg_train), len(neu_train))
print("TEST", len(pos_test), len(neg_test), len(neu_test))
print("VAL", len(pos_val), len(neg_val), len(neu_val))

train_texts = []
train_texts.extend(pos_train)
train_texts.extend(neg_train)
train_texts.extend(neu_train)

train_labels=[2]*len(pos_train)
train_labels.extend([0]*len(neg_train))
train_labels.extend([1]*len(neu_train))

c = list(zip(train_texts, train_labels))
random.shuffle(c)

train_texts, train_labels = zip(*c)
train_texts, train_labels = list(train_texts), list(train_labels)
print(len(train_texts),len(train_labels))

val_texts = []
val_texts.extend(pos_val) 
val_texts.extend(neg_val)
val_texts.extend(neu_val)

val_labels = [2]*len(pos_val)
val_labels.extend([1]*len(neg_val))
val_labels.extend([0]*len(neu_val))

c = list(zip(val_texts, val_labels))
random.shuffle(c)

val_texts, val_labels = zip(*c)
val_texts, val_labels = list(val_texts), list(val_labels)
print(len(val_texts), len(val_labels))

class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        if self.labels:
            item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.encodings["input_ids"])

    
def tokenize_function(text_list):
    # device = "cuda:0" if torch.cuda.is_available() else "cpu"
    # return tokenizer(text_list,padding="max_length",return_tensors='pt', truncation=True,max_length=HYPERPARAMS["MAX_LEN"]).to(device)
    
    return tokenizer(text_list,padding="max_length",return_tensors='pt', truncation=True,max_length=HYPERPARAMS["MAX_LEN"])

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)

    acc = accuracy_score(labels,predictions)
    pre = precision_score(labels,predictions, average='macro')
    rec = recall_score(labels,predictions, average='macro')
    f1 = f1_score(labels,predictions, average='macro')
    crp = classification_report(labels, predictions,output_dict=True)
    return {"accuracy": acc, "precision": pre, "recall": rec, "f1": f1,"classification_report_dict":crp}



## use vinai/bertweet-base for bertwteet.
# task='sentiment'
# device = "cuda:0" if torch.cuda.is_available() else "cpu"
# print(f"Device : {device}")
MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL, normalization=True,padding=True)
model = AutoModelForSequenceClassification.from_pretrained(MODEL, 
                                                           num_labels=3)
model.to("cuda:0")
X_train_tokenized = tokenize_function(train_texts)
X_val_tokenized = tokenize_function(val_texts)
train_dataset = Dataset(X_train_tokenized, train_labels)
val_dataset = Dataset(X_val_tokenized, val_labels)

from huggingface_hub import notebook_login

notebook_login()

repo_name = "finetuning-sentiment-model-25000-samples"
training_args = TrainingArguments(output_dir=repo_name,
                                  overwrite_output_dir=True, 
                                  do_train=True,
                                  do_eval=True,
                                  per_device_train_batch_size=HYPERPARAMS["BATCH_SIZE"],
                                  per_device_eval_batch_size=HYPERPARAMS["BATCH_SIZE"],
                                  learning_rate=HYPERPARAMS["LEARNING_RATE"],
                                  num_train_epochs=HYPERPARAMS["EPOCHS"],
                                  seed=HYPERPARAMS["RNG_SEED"],
                                  evaluation_strategy="epoch", 
                                  save_strategy="epoch",
                                  push_to_hub=True)

trainer = Trainer(model=model, args=training_args, train_dataset=train_dataset, eval_dataset=val_dataset,compute_metrics=compute_metrics)

trainer.train()

trainer.evaluate()

trainer.push_to_hub()

from transformers import pipeline

sentiment_model = pipeline(model="federicopascual/finetuning-sentiment-model-3000-samples")

sentiment_model(["I love this move", "This movie sucks!"])

