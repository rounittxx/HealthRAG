"""
BM25 index over all chunk texts using rank_bm25.
BM25 handles exact medical term matches better than dense embeddings —
so combining it with FAISS retrieval gives noticeably better results.
"""

import os
import json
import pickle
from rank_bm25 import BM25Okapi

BM25_INDEX_PATH = "data/processed/bm25_index.pkl"
META_PATH = "data/processed/chunks_meta.json"


def tokenise(text):
    """Simple whitespace tokeniser. Good enough for BM25."""
    return text.lower().split()


def build_bm25_index(meta):
    """Build BM25 from chunk texts and save to disk."""
    print(f"Building BM25 index over {len(meta)} chunks...")
    corpus = [tokenise(rec["text"]) for rec in meta]
    bm25 = BM25Okapi(corpus)

    with open(BM25_INDEX_PATH, "wb") as f:
        pickle.dump({"bm25": bm25, "meta": meta}, f)

    print(f"BM25 index saved to {BM25_INDEX_PATH}")
    return bm25, meta


def load_bm25_index():
    """Load pre-built BM25 index from disk."""
    if not os.path.exists(BM25_INDEX_PATH):
        raise FileNotFoundError(f"BM25 index not found at {BM25_INDEX_PATH}. Run build_bm25_index() first.")

    with open(BM25_INDEX_PATH, "rb") as f:
        data = pickle.load(f)

    return data["bm25"], data["meta"]


def bm25_search(query, bm25, meta, top_k=10):
    """
    Search BM25 index. Returns list of (chunk_text, score) tuples sorted by score.
    """
    tokens = tokenise(query)
    scores = bm25.get_scores(tokens)

    # get top_k indices sorted by score
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

    results = []
    for idx in top_indices:
        if scores[idx] > 0:  # skip zero-score results
            results.append({
                "text": meta[idx]["text"],
                "source_url": meta[idx].get("source_url", ""),
                "category": meta[idx].get("category", ""),
                "bm25_score": float(scores[idx]),
                "chunk_id": idx,
            })

    return results


if __name__ == "__main__":
    if not os.path.exists(META_PATH):
        print(f"[!] Need {META_PATH} — run embed_chunks.py first")
    else:
        with open(META_PATH) as f:
            meta = json.load(f)

        bm25, meta = build_bm25_index(meta)

        # test it
        test_query = "symptoms of diabetes type 2"
        results = bm25_search(test_query, bm25, meta, top_k=3)
        print(f"\nTop results for: '{test_query}'")
        for r in results:
            print(f"  Score {r['bm25_score']:.3f}: {r['text'][:80]}...")
