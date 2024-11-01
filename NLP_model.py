from transformers import AutoTokenizer, AutoModelForTokenClassification, Trainer, TrainingArguments, DataCollatorForTokenClassification
from datasets import load_dataset

# Завантаження моделі та токенайзера
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
model = AutoModelForTokenClassification.from_pretrained("bert-base-cased", num_labels=3)

# Додавання id2label для полегшення відображення лейблів
model.config.id2label = {0: "O", 1: "ORG", 2: "PER"}
model.config.label2id = {"O": 0, "ORG": 1, "PER": 2}

# Завантаження датасету
dataset = load_dataset('conll2003', trust_remote_code=True)
data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

# Токенізація з підгонкою міток
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples['tokens'], truncation=True, is_split_into_words=True)

    # Підгонка міток
    labels = []
    for i, label in enumerate(examples["ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)  # Отримуємо id для відповідності токенів
        aligned_labels = []
        previous_word_idx = None
        for word_idx in word_ids:
            if word_idx is None:
                aligned_labels.append(-100)
            elif word_idx != previous_word_idx:
                aligned_labels.append(label[word_idx])
            else:
                aligned_labels.append(-100)  # Для сабтокенів тієї ж лексеми
            previous_word_idx = word_idx
        labels.append(aligned_labels)

    tokenized_inputs["labels"] = labels
    return tokenized_inputs

# Токенізація всього датасету
tokenized_datasets = dataset.map(tokenize_and_align_labels, batched=True)
small_train_dataset = tokenized_datasets["train"].select(range(13000))

# Налаштування параметрів тренування
training_args = TrainingArguments(
    output_dir="./result_model",
    evaluation_strategy="epoch",
    per_device_train_batch_size=4,
    num_train_epochs=5,
    learning_rate=5e-5,
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

# Запуск тренування
trainer.train()

# Збереження моделі
model.save_pretrained("my_custom_model3")
tokenizer.save_pretrained("my_custom_model3")
