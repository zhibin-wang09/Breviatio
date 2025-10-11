from transformers import AutoTokenizer
from datasets import load_dataset

# Fine tuning the model for multi-class classification

dataset = load_dataset('')

tokenizer = AutoTokenizer.from_pretrained('distill/bert')

# we need to tokenize the inputs in order for the models to digest
def tokenize(examples):
    return tokenizer(examples['text'], padding = "max_length", truncation = True)

dataset = dataset.map(tokenize, batched=True)

