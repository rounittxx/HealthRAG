"""
Inference module for the trained symptom classifier.
Load the model once with load_classifier(), then call classify_symptoms() freely.
"""

import os
import json
import torch
from torch import nn
from transformers import AutoTokenizer, AutoModel

SAVE_DIR = "models/symptom_classifier"
CATEGORIES_PATH = "data/processed/classifier/categories.json"

# module-level cache
_classifier_cache = {}


def load_classifier():
    """Load the saved BioBERT classifier and return (model, tokenizer, categories)."""
    global _classifier_cache
    if _classifier_cache:
        return _classifier_cache

    if not os.path.exists(SAVE_DIR):
        raise FileNotFoundError(
            f"No saved classifier at {SAVE_DIR}. Run train_classifier.py first."
        )

    with open(CATEGORIES_PATH) as f:
        categories = json.load(f)

    tokenizer = AutoTokenizer.from_pretrained(SAVE_DIR)
    bert = AutoModel.from_pretrained(SAVE_DIR)

    # recreate the classifier head
    classifier_head = nn.Linear(bert.config.hidden_size, len(categories))
    head_path = os.path.join(SAVE_DIR, "classifier_head.pt")
    classifier_head.load_state_dict(torch.load(head_path, map_location="cpu"))

    device = "cuda" if torch.cuda.is_available() else "cpu"
    bert = bert.to(device)
    classifier_head = classifier_head.to(device)
    bert.eval()
    classifier_head.eval()

    _classifier_cache = {
        "bert": bert,
        "classifier_head": classifier_head,
        "tokenizer": tokenizer,
        "categories": categories,
        "device": device,
    }

    print(f"Classifier loaded. {len(categories)} ICD-10 categories.")
    return _classifier_cache


def classify_symptoms(text, threshold=0.5):
    """
    Classify symptom text and return predicted ICD-10 categories above threshold.
    # threshold of 0.5 is a starting point — lower it if you want more recall

    Returns list of (icd_category, confidence) tuples, sorted by confidence.
    If nothing is above threshold, returns [("Unknown", 0.0)] with a message.
    """
    cache = load_classifier()
    bert = cache["bert"]
    classifier_head = cache["classifier_head"]
    tokenizer = cache["tokenizer"]
    categories = cache["categories"]
    device = cache["device"]

    encoding = tokenizer(
        text,
        max_length=128,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = bert(**encoding)
        cls_output = outputs.last_hidden_state[:, 0, :]
        logits = classifier_head(cls_output)
        probs = torch.sigmoid(logits).cpu().numpy()[0]

    results = []
    for cat, prob in zip(categories, probs):
        if prob >= threshold:
            results.append((cat, float(prob)))

    if not results:
        print(f"[low confidence] No category above {threshold} for: '{text[:60]}'")
        print("  Consider lowering threshold or using a General Physician.")
        return [("Unknown", 0.0)]

    return sorted(results, key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    test_inputs = [
        "I have a persistent cough and shortness of breath",
        "severe headache and sensitivity to light",
        "excessive thirst, frequent urination, and fatigue",
    ]

    print("Testing classifier...\n")
    for text in test_inputs:
        print(f"Input: {text}")
        results = classify_symptoms(text)
        for cat, conf in results:
            print(f"  {cat}: {conf:.3f}")
        print()
