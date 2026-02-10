"""
Builds a FAISS index from the pre-generated embeddings.
Run after embed_chunks.py.
"""

import os
import json
import numpy as np
import faiss

EMBEDDINGS_PATH = "data/processed/embeddings.npy"
META_PATH = "data/processed/chunks_meta.json"
INDEX_PATH = "data/processed/medquad.index"


def build_index(embeddings):
    """
    Build a flat L2 index. Good for < 50K vectors without any approximation.
    # TODO: switch to IndexIVFFlat when dataset grows beyond 100K vectors
    """
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype(np.float32))
    return index


def sanity_check(index, embeddings, meta):
    """Quick check: take first chunk, find its 3 nearest neighbours."""
    print("\nSanity check: searching nearest neighbours of the first chunk...")
    query_vec = embeddings[0:1].astype(np.float32)
    distances, indices = index.search(query_vec, 3)

    for rank, (dist, idx) in enumerate(zip(distances[0], indices[0])):
        chunk_text = meta[idx]["text"][:100]
        print(f"  #{rank+1} (dist={dist:.4f}): {chunk_text}...")


def main():
    if not os.path.exists(EMBEDDINGS_PATH):
        print(f"[!] Embeddings not found at {EMBEDDINGS_PATH}")
        print("    Run embed_chunks.py first")
        return

    print(f"Loading embeddings from {EMBEDDINGS_PATH}...")
    embeddings = np.load(EMBEDDINGS_PATH)
    print(f"Embeddings shape: {embeddings.shape}")

    print("Loading chunk metadata...")
    with open(META_PATH) as f:
        meta = json.load(f)

    print("Building FAISS index...")
    index = build_index(embeddings)
    print(f"Vectors indexed: {index.ntotal}")

    faiss.write_index(index, INDEX_PATH)
    print(f"Index saved to {INDEX_PATH}")

    sanity_check(index, embeddings, meta)

    print("\nDone! The FAISS index is ready for retrieval.")


if __name__ == "__main__":
    main()
