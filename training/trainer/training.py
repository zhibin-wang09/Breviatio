import glob
from server.models.label import category_to_number
from transformers import AutoTokenizer, DataCollatorWithPadding, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import numpy as np
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Machine is learning...")

email_trianing_data = {
    'text': [],
    'label': []
}
files = glob.glob("training/emails/email*.txt")
files.sort(key=lambda f: int(f.split("_")[1].split(".")[0]))
count = 0

    
# reading files and put them into a dictionary format
logging.info("Data gathering...")
for file_path in files:
    if count == 10:
        break
    
    count += 1    
    
    with open(file_path, "r", encoding="utf-8") as file:
        category = file_path.split("_")[2].split(".")[0]
        email_trianing_data['text'].append(file.read())
        email_trianing_data['label'].append(category_to_number(category))

        
# set up tokenizer and dataset
# tokenizer for the model to understand human language
# dataset for the model to train/test on
logging.info("Set up the tokenizer & model...")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
dataset = Dataset.from_dict(email_trianing_data)
split_dataset = dataset.train_test_split(test_size=0.2)

def preprocess_function(examples):
    return tokenizer(examples["text"], truncation = True)

tokenized_dataset = split_dataset.map(preprocess_function, batched = True)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# select a model for fine tuning
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=7)

# set up training argument
logging.info("Set up the training argument and trainer...")
training_args= TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=5,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# training
logging.info("Training...")
trainer.train()

# use the model to make predictions
predictions = trainer.predict(tokenized_dataset["test"])


logits = predictions.predictions
predicted_labels = np.argmax(logits, axis=-1)
print(predicted_labels)