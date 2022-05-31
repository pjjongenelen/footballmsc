"""
THIS CODE DOES NOT RUN
It is based on the HF documentation of fine-tuning a pre-trained model https://huggingface.co/docs/transformers/training#train-in-native-pytorch
however, this returns a common error.
"""

import eredivisie_nlp as enlp
from datasets import load_metric, load_dataset
import json
import numpy as np
import pandas as pd
from pathlib import Path
from random import shuffle
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import TrainingArguments, Trainer

# load RobBERT model
tokenizer = AutoTokenizer.from_pretrained("pdelobelle/robbert-v2-dutch-base")
model = AutoModelForSequenceClassification.from_pretrained("pdelobelle/robbert-v2-dutch-base", num_labels=7)

# put data in huggingface format and save to json
if not Path(f"{enlp.determine_root()}/data/tweets_hf_train.json").exists() or Path(
        f"{enlp.determine_root()}/data/tweets_hf_test.json").exists():
    dataset = pd.read_excel(f"{enlp.determine_root()}/data/sentiment_annotations.xlsx")
    dataset = dataset[dataset.annotation != 100]
    data = [{'label': annotation, 'text': sentence} for annotation, sentence in
            zip(dataset.annotation, dataset.sentence)]
    shuffle(data)
    hf_data_train = {'version': '1.0', 'data': data[:900]}
    hf_data_test = {'version': '1.0', 'data': data[900:]}
    with open(f"{enlp.determine_root()}/data/tweets_hf_train.json", "w") as f:
        json.dump(hf_data_train, f)
    with open(f"{enlp.determine_root()}/data/tweets_hf_test.json", "w") as f:
        json.dump(hf_data_test, f)

# load data
dataset = load_dataset('json', data_files=f"{enlp.determine_root()}/data/tweets_hf_train.json", field='data')
dataset = dataset['train']
dataset = dataset.train_test_split(test_size=0.2, seed=42)


# tokenize
def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True)


tokenized_datasets = dataset.map(tokenize_function, batched=True)

# load default training arguments and a metric
training_args = TrainingArguments(output_dir="test_trainer")
metric = load_metric("mae")


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=1)
    return metric.compute(predictions=predictions, references=labels)


train_data = tokenized_datasets['train'].shuffle(seed=42)
eval_data = tokenized_datasets['test'].shuffle(seed=42)


# create a trainer object
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_data,
    eval_dataset=eval_data,
    compute_metrics=compute_metrics,
)
trainer.train()
