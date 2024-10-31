from transformers import AutoTokenizer, AutoModelForTokenClassification, Trainer, TrainingArguments, DataCollatorForTokenClassification
from datasets import load_dataset

# Завантаження моделі та токенайзера
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-cased")
model = AutoModelForTokenClassification.from_pretrained("distilbert-base-cased", num_labels=3)

# Завантаження датасету
dataset = load_dataset('conll2003', trust_remote_code=True)
data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

# Токенізація з підгонкою міток
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples['tokens'], truncation=True, is_split_into_words=True)
    tokenized_inputs["labels"] = examples["ner_tags"]
    return tokenized_inputs

# Токенізація всього датасету
tokenized_datasets = dataset.map(tokenize_and_align_labels, batched=True)
small_train_dataset = tokenized_datasets["train"].select(range(1000))
# Налаштування параметрів тренування
training_args = TrainingArguments(
    output_dir="./result_model",
    evaluation_strategy="epoch",
    per_device_train_batch_size=8,
    num_train_epochs=2,
    weight_decay=0.01,
    logging_strategy="steps",
    logging_steps=100,
    logging_dir=None,
)

# Ініціалізація Trainer з правильними параметрами
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=small_train_dataset,
    eval_dataset=tokenized_datasets["validation"],
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# Перевірка структури датасету для одного прикладу
print(tokenized_datasets["train"][0])

# Запуск тренування
trainer.train()

# Збереження моделі
model.save_pretrained("my_custom_model1")
