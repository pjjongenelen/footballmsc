import eredivisie_nlp as enlp
from datasets import load_dataset
import json
import pandas as pd
from pathlib import Path
from random import shuffle
import torch
from torch.optim import AdamW
from torch.utils.data import DataLoader
from tqdm.auto import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification, get_scheduler

# global variables
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("pdelobelle/robbert-v2-dutch-base")

# functions
def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True)

# main code
# check if a formatted data file exist
if not Path(f"{enlp.determine_root()}/data/tweets_hf_train.json").exists() or not Path(
        f"{enlp.determine_root()}/data/tweets_hf_test.json").exists():
    # put data in huggingface format and save to json
    print("No formatted data found, transforming data to HF format...")
    dataset = pd.read_excel(f"{enlp.determine_root()}/data/sentiment_annotations.xlsx")
    dataset = dataset[dataset.annotation != 100]
    data = [{'label': annotation, 'text': sentence} for annotation, sentence in
            zip(dataset.annotation_std, dataset.sentence)]
    shuffle(data)
    hf_data_train = {'version': '1.0', 'data': data[:900]}
    hf_data_test = {'version': '1.0', 'data': data[900:]}
    with open(f"{enlp.determine_root()}/data/tweets_hf_train.json", "w") as f:
        json.dump(hf_data_train, f)
    with open(f"{enlp.determine_root()}/data/tweets_hf_test.json", "w") as f:
        json.dump(hf_data_test, f)
# load data
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

small_train_dataset = tokenized_datasets['train'].shuffle(seed=42).select(range(len(tokenized_datasets['train'])))
small_eval_dataset = tokenized_datasets['test'].shuffle(seed=42).select(range(len(tokenized_datasets['test'])))

# create torch data loaders
train_dataloader = DataLoader(small_train_dataset, shuffle=True, batch_size=4)
eval_dataloader = DataLoader(small_eval_dataset, batch_size=8)

# load model
model = AutoModelForSequenceClassification.from_pretrained("pdelobelle/robbert-v2-dutch-base", num_labels=7)

# optimizer and lr
optimizer = AdamW(model.parameters(), lr=5e-5)
num_epochs = 3
num_training_steps = num_epochs * len(train_dataloader)
lr_scheduler = get_scheduler(
    name="linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=num_training_steps
)

# specify device
device = torch.device("cuda")
model.to(device)

# training loop
progress_bar = tqdm(range(num_training_steps))
model.train()
for epoch in range(num_epochs):
    for batch in train_dataloader:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()

        optimizer.step()
        lr_scheduler.step()
        optimizer.zero_grad()
        progress_bar.update(1)
