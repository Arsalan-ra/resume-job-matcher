"""Fine-tune bert-base-uncased to classify resumes into job categories.

Dataset: UpdatedResumeDataSet.csv (columns: "Category", "Resume"), expected at
backend/data/UpdatedResumeDataSet.csv. Splits 80/20 train/validation, trains
with HuggingFace Trainer, and saves the best checkpoint (by validation
accuracy) to backend/data/model/.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)
import torch
from torch.utils.data import Dataset

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATASET_PATH = DATA_DIR / "UpdatedResumeDataSet.csv"
MODEL_OUTPUT_DIR = DATA_DIR / "model"
BASE_MODEL_NAME = "bert-base-uncased"
MAX_LENGTH = 256
NUM_EPOCHS = 3
TRAIN_BATCH_SIZE = 8
EVAL_BATCH_SIZE = 16


def clean_text(text: str) -> str:
    """Strip URLs, punctuation, and excess whitespace from raw resume text."""
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


class ResumeDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        item = {key: tensor[index] for key, tensor in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[index])
        return item


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    accuracy = (predictions == labels).mean()
    return {"accuracy": float(accuracy)}


def main():
    df = pd.read_csv(DATASET_PATH)
    df["Resume"] = df["Resume"].apply(clean_text)

    label_encoder = LabelEncoder()
    df["label"] = label_encoder.fit_transform(df["Category"])

    train_df, val_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df["label"]
    )

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)
    train_encodings = tokenizer(
        train_df["Resume"].tolist(),
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )
    val_encodings = tokenizer(
        val_df["Resume"].tolist(),
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )

    train_dataset = ResumeDataset(train_encodings, train_df["label"].tolist())
    val_dataset = ResumeDataset(val_encodings, val_df["label"].tolist())

    model = AutoModelForSequenceClassification.from_pretrained(
        BASE_MODEL_NAME, num_labels=len(label_encoder.classes_)
    )

    training_args = TrainingArguments(
        output_dir=str(MODEL_OUTPUT_DIR / "checkpoints"),
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=TRAIN_BATCH_SIZE,
        per_device_eval_batch_size=EVAL_BATCH_SIZE,
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=1,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        logging_strategy="epoch",
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
    )

    trainer.train()

    eval_results = []
    for log in trainer.state.log_history:
        if "eval_accuracy" in log:
            eval_results.append((log["epoch"], log["eval_accuracy"]))
            print(f"Epoch {log['epoch']:.0f} validation accuracy: {log['eval_accuracy']:.4f}")

    final_accuracy = eval_results[-1][1] if eval_results else 0.0
    best_accuracy = max(acc for _, acc in eval_results) if eval_results else 0.0

    MODEL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    trainer.save_model(str(MODEL_OUTPUT_DIR))
    tokenizer.save_pretrained(str(MODEL_OUTPUT_DIR))

    print(f"\nBest model saved to: {MODEL_OUTPUT_DIR}")
    print(f"FINAL VALIDATION ACCURACY: {final_accuracy:.4f}")
    print(f"BEST VALIDATION ACCURACY: {best_accuracy:.4f}")


if __name__ == "__main__":
    main()
