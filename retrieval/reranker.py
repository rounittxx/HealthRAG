"""
Cross-encoder reranker using ms-marco-MiniLM.
Reranking bumped my Precision@5 from 0.61 to 0.73 — worth the extra 0.3s latency.
"""

from sentence_transformers import CrossEncoder

RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# load once when module is imported — not per call
_reranker = None


def get_reranker():
    global _reranker
    if _reranker is None:
        print(f"Loading reranker: {RERANKER_MODEL}")
        _reranker = CrossEncoder(RERANKER_MODEL)
    return _reranker


def rerank(query, candidates):
    """
    Score each (query, chunk) pair with the cross-encoder.
    Returns candidates sorted by reranking score (best first).

    candidates: list of dicts, each with a 'text' key
    """
    if not candidates:
        return candidates

    reranker = get_reranker()

    # build pairs for scoring
    pairs = [(query, c["text"]) for c in candidates]
    scores = reranker.predict(pairs)

    # attach score and sort
    for i, c in enumerate(candidates):
        c["rerank_score"] = float(scores[i])

    return sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)


if __name__ == "__main__":
    test_query = "what are the symptoms of asthma?"
    dummy_candidates = [
        {"text": "Asthma causes wheezing, shortness of breath and chest tightness.", "source_url": "pubmed.ncbi.nlm.nih.gov/1"},
        {"text": "Hypertension is high blood pressure affecting the cardiovascular system.", "source_url": "pubmed.ncbi.nlm.nih.gov/2"},
        {"text": "During an asthma attack, airways narrow and swell.", "source_url": "nhs.uk/asthma"},
    ]

    ranked = rerank(test_query, dummy_candidates)
    print("Reranked results:")
    for r in ranked:
        print(f"  Score {r['rerank_score']:.4f}: {r['text'][:80]}")
