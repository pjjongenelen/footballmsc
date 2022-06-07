"""
Fine-tunes the RobBERT model using the hand-annotated data
Based on the HF documentation https://huggingface.co/docs/transformers/training#train-in-native-pytorch
"""

import eredivisie_nlp as enlp
from datasets import load_dataset
import json
import matplotlib.pyplot as plt
import pandas as pd
import torch
from torch.optim import AdamW
from torch.utils.data import DataLoader
from tqdm.auto import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification, get_scheduler

SAVE = 0  # set to 1 if new model needs to be saved, 0 while debugging
FRAC = 1  # fraction of dataset to use. Defined as 1/FRAC, so 2 means half the data
tokenizer = AutoTokenizer.from_pretrained("pdelobelle/robbert-v2-dutch-base")


def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True)


# put data in huggingface format
print("Transforming data to HF format...")
dataset = pd.read_excel(f"{enlp.determine_root()}/data/sentiment_annotations_noleakage.xlsx")
dataset = dataset[dataset.annotation != 100]
data = [{'label': annotation, 'text': text} for annotation, text in
        zip(dataset.annotation_std, dataset.text)]

# make train test split and save to JSON
train_test_cutoff = int(len(data) * 0.9)
hf_data_train = {'version': '1.0', 'data': data[:train_test_cutoff]}
hf_data_test = {'version': '1.0', 'data': data[train_test_cutoff:]}
with open(f"{enlp.determine_root()}/data/tweets_hf_train.json", "w") as f:
    json.dump(hf_data_train, f)
with open(f"{enlp.determine_root()}/data/tweets_hf_test.json", "w") as f:
    json.dump(hf_data_test, f)

# load formatted data
print("Loading data...")
dataset = load_dataset('json', data_files=f"{enlp.determine_root()}/data/tweets_hf_train.json", field='data')
dataset = dataset['train']
dataset = dataset.train_test_split(test_size=0.2, seed=42)

# tokenize
print("Tokenizing dataset...")
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# postprocess
print("Postprocessing data...")
tokenized_datasets = tokenized_datasets.remove_columns(["text"])
tokenized_datasets = tokenized_datasets.rename_column("label", "labels")
tokenized_datasets.set_format("torch")

# unnecessary lines, but kept to be able to copy straight from the HF docs for v1
small_train_dataset = tokenized_datasets['train'].shuffle(seed=42).select(
    range(int(len(tokenized_datasets['train']) / FRAC)))
small_eval_dataset = tokenized_datasets['test'].shuffle(seed=42).select(
    range(int(len(tokenized_datasets['test']) / FRAC)))

# create torch data loaders
train_dataloader = DataLoader(small_train_dataset, shuffle=True, batch_size=4)
eval_dataloader = DataLoader(small_eval_dataset, batch_size=4)

# load model
model = AutoModelForSequenceClassification.from_pretrained("pdelobelle/robbert-v2-dutch-base", num_labels=7)

# optimizer and lr
optimizer = AdamW(model.parameters(), lr=5e-5)
num_epochs = 3
num_training_steps = num_epochs * len(train_dataloader)
lr_scheduler = get_scheduler(name="linear", optimizer=optimizer, num_warmup_steps=0,
                             num_training_steps=num_training_steps)

# specify device
device = torch.device("cuda")
model.to(device)

# training loop
progress_bar = tqdm(range(num_training_steps))
model.train()
losses = []
for epoch in range(num_epochs):
    for batch in train_dataloader:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss
        losses.append(loss.item())
        loss.backward()

        optimizer.step()
        lr_scheduler.step()
        optimizer.zero_grad()
        progress_bar.update(1)

if SAVE:
    model.save_pretrained(f'./robbert_{int(len(data) / FRAC)}')

plt.plot(losses)
plt.show()
