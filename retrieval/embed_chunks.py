"""
Generates Bio_ClinicalBERT embeddings for all cleaned chunks and saves them.
Run after clean_text.py has produced data/processed/cleaned_chunks.json
"""

import os
import json
import argparse
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

# model choice: Bio_ClinicalBERT gives 768-dim embeddings tailored for clinical text
MODEL_NAME = "emilyalsentzer/Bio_ClinicalBERT"
BATCH_SIZE = 32  # batching prevents OOM — learned this the hard way
CHUNKS_PATH = "data/processed/cleaned_chunks.json"
OUT_EMBEDDINGS = "data/processed/embeddings.npy"
OUT_META = "data/processed/chunks_meta.json"


def mean_pool(model_output, attention_mask):
    """Mean pool token embeddings, ignoring padding tokens."""
    token_embeddings = model_output.last_hidden_state
    # expand mask to match embedding dim
    mask = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    summed = torch.sum(token_embeddings * mask, dim=1)
    counts = torch.clamp(mask.sum(dim=1), min=1e-9)
    return summed / counts


def embed_chunks(texts, tokenizer, model, device):
    """Embed a batch of text strings. Returns numpy array of shape (n, 768)."""
    encoded = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        output = model(**encoded)

    embeddings = mean_pool(output, encoded["attention_mask"])
    return embeddings.cpu().numpy()


def main(subset=None):
    os.makedirs("data/processed", exist_ok=True)

    print(f"Loading chunks from {CHUNKS_PATH}...")
    with open(CHUNKS_PATH) as f:
        chunks = json.load(f)

    if subset:
        chunks = chunks[:subset]
        print(f"[subset mode] Using first {subset} chunks")

    print(f"Total chunks to embed: {len(chunks)}")

    print(f"Loading {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    model = model.to(device)
    model.eval()

    all_embeddings = []
    texts = [c["text"] for c in chunks]

    print("Generating embeddings...")
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        batch_embeddings = embed_chunks(batch, tokenizer, model, device)
        all_embeddings.append(batch_embeddings)

        if i % 500 == 0 and i > 0:
            print(f"  Embedded {i}/{len(texts)} chunks...")

    all_embeddings = np.vstack(all_embeddings)
    print(f"Final embedding matrix shape: {all_embeddings.shape}")

    # save embeddings as numpy binary (fast to load later)
    np.save(OUT_EMBEDDINGS, all_embeddings)
    print(f"Embeddings saved to {OUT_EMBEDDINGS}")

    # save metadata so we can map embedding index → chunk text + source
    meta = [
        {
            "text": c["text"],
            "source_url": c.get("source_url", ""),
            "category": c.get("category", ""),
            "original_question": c.get("original_question", ""),
        }
        for c in chunks
    ]
    with open(OUT_META, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"Chunk metadata saved to {OUT_META}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subset", type=int, default=None,
                        help="Only embed first N chunks (for testing)")
    args = parser.parse_args()
    main(subset=args.subset)
