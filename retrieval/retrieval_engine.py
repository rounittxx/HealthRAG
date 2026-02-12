"""
Main retrieval engine — loads FAISS + BM25 + the BERT model, and provides
hybrid search that blends both scores.
"""

import os
import json
import numpy as np
import faiss
import torch
from transformers import AutoTokenizer, AutoModel

from retrieval.bm25_index import load_bm25_index, bm25_search, build_bm25_index

MODEL_NAME = "emilyalsentzer/Bio_ClinicalBERT"

FAISS_INDEX_PATH = "data/processed/medquad.index"
META_PATH = "data/processed/chunks_meta.json"
EMBEDDINGS_PATH = "data/processed/embeddings.npy"

# weights for hybrid score: tried 0.5/0.5 but dense was stronger
DENSE_WEIGHT = 0.6
BM25_WEIGHT = 0.4

# module-level cache so we don't reload models on every call
_resources = {}


def load_resources():
    """
    Load everything once at startup: FAISS index, metadata, BM25 index, BERT model.
    Calling this multiple times is fine — it checks if already loaded.
    """
    global _resources
    if _resources:
        return _resources

    print("Loading retrieval resources...")

    # FAISS index
    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError(f"FAISS index not found: {FAISS_INDEX_PATH}")
    index = faiss.read_index(FAISS_INDEX_PATH)
    print(f"  FAISS index loaded: {index.ntotal} vectors")

    # chunk metadata
    with open(META_PATH) as f:
        meta = json.load(f)

    # embeddings (needed for cosine similarity scoring)
    embeddings = np.load(EMBEDDINGS_PATH).astype(np.float32)

    # BM25
    try:
        bm25, _ = load_bm25_index()
    except FileNotFoundError:
        print("  BM25 index not found, building it now...")
        bm25, _ = build_bm25_index(meta)

    # BERT tokenizer + model for embedding queries
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    model.eval()
    print(f"  BERT model loaded on {device}")

    _resources = {
        "index": index,
        "meta": meta,
        "embeddings": embeddings,
        "bm25": bm25,
        "tokenizer": tokenizer,
        "model": model,
        "device": device,
    }

    return _resources


def embed_query(query_text):
    """Embed a single query string using Bio_ClinicalBERT."""
    r = load_resources()
    tokenizer, model, device = r["tokenizer"], r["model"], r["device"]

    encoded = tokenizer(
        query_text,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        output = model(**encoded)

    # mean pool
    token_emb = output.last_hidden_state
    mask = encoded["attention_mask"].unsqueeze(-1).expand(token_emb.size()).float()
    query_vec = (torch.sum(token_emb * mask, dim=1) / torch.clamp(mask.sum(dim=1), min=1e-9))
    return query_vec.cpu().numpy().astype(np.float32)


def dense_search(query_vec, top_k=10):
    """Search FAISS for top_k nearest neighbours. Returns list of chunk dicts."""
    r = load_resources()
    distances, indices = r["index"].search(query_vec, top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < 0:
            continue
        chunk = dict(r["meta"][idx])
        # convert L2 distance to a 0-1 similarity score (lower dist = higher sim)
        chunk["dense_score"] = float(1 / (1 + dist))
        chunk["chunk_id"] = int(idx)
        results.append(chunk)

    return results


def hybrid_search(query_text, top_k=5):
    """
    Combines dense FAISS + BM25 scores with a weighted sum.
    Dense: 0.6, BM25: 0.4 — this blend worked well in practice.
    """
    r = load_resources()

    query_vec = embed_query(query_text)
    dense_results = dense_search(query_vec, top_k=top_k * 2)  # get more, then re-rank
    bm25_results = bm25_search(query_text, r["bm25"], r["meta"], top_k=top_k * 2)

    # merge by chunk_id
    scores = {}

    # normalise dense scores (already 0-1 from our conversion)
    for res in dense_results:
        cid = res["chunk_id"]
        scores[cid] = {"chunk": res, "score": res["dense_score"] * DENSE_WEIGHT}

    # normalise BM25 scores (divide by max to get 0-1 range)
    max_bm25 = max((r["bm25_score"] for r in bm25_results), default=1)
    for res in bm25_results:
        cid = res["chunk_id"]
        norm_score = (res["bm25_score"] / max(max_bm25, 1e-9)) * BM25_WEIGHT
        if cid in scores:
            scores[cid]["score"] += norm_score
        else:
            scores[cid] = {"chunk": res, "score": norm_score}

    # sort by combined score
    ranked = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
    top = [item["chunk"] for item in ranked[:top_k]]

    return top


if __name__ == "__main__":
    test_queries = [
        "what are the symptoms of type 2 diabetes?",
        "how is pneumonia treated?",
        "causes of high blood pressure",
    ]

    print("Testing hybrid search with 3 queries...\n")
    for q in test_queries:
        print(f"Query: {q}")
        results = hybrid_search(q, top_k=3)
        for i, r in enumerate(results):
            print(f"  [{i+1}] {r['text'][:100]}...")
            print(f"       Source: {r.get('source_url', 'N/A')}")
        print()
