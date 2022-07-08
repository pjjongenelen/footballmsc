import eredivisie_nlp as enlp
import numpy as np
import pandas as pd
from tqdm import tqdm
from transformers import RobertaForSequenceClassification, RobertaTokenizer


device = 'lenovo_part2'
ann_path = f"{enlp.determine_root()}/data/sentiment_annotations"

if device == 'msi':
    df_man = pd.read_excel(io=f"{ann_path}_manual_no_leakage.xlsx", sheet_name='Sheet_1')[:83000]
elif device == 'lenovo':
    df_man = pd.read_excel(io=f"{ann_path}_manual_no_leakage.xlsx", sheet_name='Sheet_1')[83000:145000]
else:
    df_man = pd.read_excel(io=f"{ann_path}_manual_no_leakage.xlsx", sheet_name='Sheet_1')[145000:]


print("Assigning RobBERT scores")
model = RobertaForSequenceClassification.from_pretrained("./robbert_600")
tokenizer = RobertaTokenizer.from_pretrained("pdelobelle/robbert-v2-dutch-base")
encoded_tweets = [tokenizer(tweet, return_tensors='pt', padding='max_length', truncation=True) for tweet in
                  tqdm(df_man.text)]
outputs = [model(**et)[0].detach().numpy() for et in tqdm(encoded_tweets)]
sentiments = []
for output in outputs:
    robbert_score = np.where(output[0] == max(output[0]))[0].item()
    sentiments.append(enlp.transform_score(robbert_score))

df = pd.DataFrame({f'score_{device}': sentiments})
df.to_pickle(enlp.determine_root() + f"/data/robbert_scores/{device}.pkl")