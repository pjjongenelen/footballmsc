# from: https://huggingface.co/docs/transformers/preprocessing

#%%
# imports
from transformers import AutoTokenizer

# input
batch_sentences = [
    "But what about second breakfast?",
    "Don't think he knows about second breakfast, Pip.",
    "What about elevensies?",
]

# set up tokenizer
tokenizer = AutoTokenizer.from_pretrained("pdelobelle/robbert-v2-dutch-base")

#%%
# Pytorch
encoded_input = tokenizer(batch_sentences, padding=True, truncation=True, return_tensors="pt")
print(encoded_input)
# {'input_ids': tensor([[  101,   153,  7719, 21490,  1122,  1114,  9582,  1623,   102],
#                       [  101,  5226,  1122,  9649,  1199,  2610,  1236,   102,     0]]),
#  'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0],
#                            [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
#  'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1],
#                            [1, 1, 1, 1, 1, 1, 1, 1, 0]])}

