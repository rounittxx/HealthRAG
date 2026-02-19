"""
Fine-tune BioBERT for multi-label symptom → ICD-10 classification.
Training on CPU is slow — use Google Colab free GPU if needed.
Save the checkpoint and download it to models/symptom_classifier/
"""

import os
import json
import ast
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModel, get_linear_schedule_with_warmup
from sklearn.metrics import f1_score

# ── Config ────────────────────────────────────────────────────────────────────
MODEL_NAME = "dmis-lab/biobert-base-cased-v1.2"
BATCH_SIZE = 16
MAX_LEN = 128
EPOCHS = 5
LR = 2e-5  # standard for fine-tuning BERT

DATA_DIR = "data/processed/classifier"
SAVE_DIR = "models/symptom_classifier"
os.makedirs(SAVE_DIR, exist_ok=True)

# load categories
with open(f"{DATA_DIR}/categories.json") as f:
    CATEGORIES = json.load(f)
NUM_LABELS = len(CATEGORIES)


# ── Dataset ────────────────────────────────────────────────────────────────────

class SymptomDataset(Dataset):
    def __init__(self, df, tokenizer, max_len=MAX_LEN):
        self.texts = df["symptom_text"].tolist()
        # labels column is stored as string representation of list
        self.labels = [
            ast.literal_eval(l) if isinstance(l, str) else l
            for l in df["labels"].tolist()
        ]
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            max_length=self.max_len,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "labels": torch.tensor(self.labels[idx], dtype=torch.float),
        }


# ── Model ─────────────────────────────────────────────────────────────────────

class BioBERTClassifier(nn.Module):
    def __init__(self, num_labels):
        super().__init__()
        self.bert = AutoModel.from_pretrained(MODEL_NAME)
        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_labels)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        cls_output = outputs.last_hidden_state[:, 0, :]  # [CLS] token
        cls_output = self.dropout(cls_output)
        logits = self.classifier(cls_output)
        return logits


# ── Training Loop ─────────────────────────────────────────────────────────────

def train_epoch(model, loader, optimizer, scheduler, criterion, device):
    model.train()
    total_loss = 0

    for step, batch in enumerate(loader):
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        optimizer.zero_grad()
        logits = model(input_ids, attention_mask)
        loss = criterion(logits, labels)
        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()
        total_loss += loss.item()

        if step % 50 == 0 and step > 0:
            print(f"  Step {step}/{len(loader)}, loss: {loss.item():.4f}")

    return total_loss / len(loader)


def evaluate(model, loader, device):
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch in loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].numpy()

            logits = model(input_ids, attention_mask)
            probs = torch.sigmoid(logits).cpu().numpy()
            preds = (probs >= 0.5).astype(int)

            all_preds.extend(preds)
            all_labels.extend(labels)

    macro_f1 = f1_score(np.array(all_labels), np.array(all_preds), average="macro", zero_division=0)
    return macro_f1


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Training on: {device}")

    print("Loading data...")
    train_df = pd.read_csv(f"{DATA_DIR}/train.csv")
    val_df = pd.read_csv(f"{DATA_DIR}/val.csv")
    print(f"Train: {len(train_df)}, Val: {len(val_df)}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    train_dataset = SymptomDataset(train_df, tokenizer)
    val_dataset = SymptomDataset(val_df, tokenizer)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)

    model = BioBERTClassifier(NUM_LABELS).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=0.01)
    criterion = nn.BCEWithLogitsLoss()

    total_steps = len(train_loader) * EPOCHS
    # warmup for first 10% of steps — helps avoid early divergence
    warmup_steps = int(total_steps * 0.10)
    scheduler = get_linear_schedule_with_warmup(optimizer, warmup_steps, total_steps)

    best_f1 = 0
    for epoch in range(1, EPOCHS + 1):
        print(f"\n=== Epoch {epoch}/{EPOCHS} ===")
        avg_loss = train_epoch(model, train_loader, optimizer, scheduler, criterion, device)
        val_f1 = evaluate(model, val_loader, device)

        print(f"Epoch {epoch}: loss={avg_loss:.4f}, val_macro_F1={val_f1:.4f}")

        if val_f1 > best_f1:
            best_f1 = val_f1
            # save the model and tokenizer
            model.bert.save_pretrained(SAVE_DIR)
            tokenizer.save_pretrained(SAVE_DIR)
            # save the classifier head separately
            torch.save(model.classifier.state_dict(), f"{SAVE_DIR}/classifier_head.pt")
            print(f"  New best model saved (F1={best_f1:.4f})")

    print(f"\nTraining done. Best val macro-F1: {best_f1:.4f}")
    print(f"Model saved to {SAVE_DIR}/")

    if best_f1 >= 0.80:
        print("Target met (>= 0.80)!")
    else:
        print(f"Below target 0.80 — try more epochs or a lower learning rate")


if __name__ == "__main__":
    main()
