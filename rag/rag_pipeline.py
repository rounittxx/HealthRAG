"""
The heart of HealthRAG — pulls together retrieval, reranking, classification,
and LLM generation into one clean interface.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retrieval.retrieval_engine import hybrid_search, load_resources
from retrieval.reranker import rerank
from classifier.inference import classify_symptoms
from classifier.specialist_router import recommend_specialist
from rag.prompt_templates import (
    MEDICAL_QA_TEMPLATE,
    SAFETY_CHECK_TEMPLATE,
    LOW_CONFIDENCE_RESPONSE,
    NON_MEDICAL_RESPONSE,
    CONTEXTUAL_QA_TEMPLATE,
)
from rag.llm_client import call_llm
from config import CONFIDENCE_THRESHOLD, TOP_K_RETRIEVAL, MAX_CHAT_HISTORY


class RAGPipeline:
    def __init__(self):
        print("Initialising RAG pipeline...")

        # load retrieval resources (FAISS + BM25 + BERT)
        load_resources()
        print("  Retrieval engine ready")

        # pre-load classifier so first query isn't slow
        try:
            from classifier.inference import load_classifier
            load_classifier()
            print("  Classifier ready")
        except FileNotFoundError:
            print("  [!] Classifier model not found — classify/recommend endpoints will be limited")

        # conversation memory: simple list of (question, answer) pairs
        # keeping only last MAX_CHAT_HISTORY turns to avoid bloating the prompt
        self.chat_history = []

        print("RAG pipeline ready!\n")

    def is_medical_query(self, text):
        """
        Quick safety check — makes sure we're only answering medical questions.
        # prevents people asking me to write poems or solve maths problems
        """
        prompt = SAFETY_CHECK_TEMPLATE.format(question=text)
        try:
            response = call_llm(prompt).strip().upper()
            return response.startswith("YES")
        except Exception as e:
            print(f"  [safety check failed, defaulting to True]: {e}")
            return True  # fail open for medical safety

    def get_answer(self, query, chat_history=None):
        """
        Main entry point. Takes a user query, runs the full RAG pipeline,
        returns a dict with answer + metadata.
        """
        # check if this is even a medical question
        if not self.is_medical_query(query):
            return {
                "answer": NON_MEDICAL_RESPONSE,
                "sources": [],
                "confidence": 0.0,
                "icd_categories": [],
                "specialist": None,
            }

        # retrieve relevant chunks (hybrid: dense FAISS + BM25)
        raw_chunks = hybrid_search(query, top_k=TOP_K_RETRIEVAL * 2)

        # rerank to push the most relevant chunks to the top
        top_chunks = rerank(query, raw_chunks)[:TOP_K_RETRIEVAL]

        # confidence = highest retrieval similarity score
        confidence = max((c.get("rerank_score", c.get("dense_score", 0)) for c in top_chunks), default=0)

        # if confidence is too low, don't try to answer — just redirect to a doctor
        if confidence < CONFIDENCE_THRESHOLD:
            return {
                "answer": LOW_CONFIDENCE_RESPONSE,
                "sources": [],
                "confidence": confidence,
                "icd_categories": [],
                "specialist": "General Physician",
            }

        # build context string with source citations
        context_parts = []
        sources = []
        for i, chunk in enumerate(top_chunks):
            src = chunk.get("source_url", "Unknown source")
            context_parts.append(f"[Source {i+1}: {src}]\n{chunk['text']}")
            if src and src not in sources:
                sources.append(src)

        context = "\n\n".join(context_parts)

        # build the full prompt — use contextual template when history is present
        history = chat_history if chat_history is not None else self.chat_history
        if history:
            history_text = "\n".join(
                f"User: {q}\nAssistant: {a}"
                for q, a in history[-MAX_CHAT_HISTORY:]
            )
            prompt = CONTEXTUAL_QA_TEMPLATE.format(
                history=history_text,
                context=context,
                question=query,
            )
        else:
            prompt = MEDICAL_QA_TEMPLATE.format(
                context=context,
                question=query,
            )

        # call the LLM
        try:
            answer = call_llm(prompt)
        except Exception as e:
            answer = f"I ran into an issue generating a response: {e}. Please try again."

        # classify the symptoms mentioned in the query
        try:
            icd_results = classify_symptoms(query)
            icd_categories = [cat for cat, _ in icd_results if cat != "Unknown"]
            specialist, _ = recommend_specialist(icd_results)
        except Exception:
            icd_categories = []
            specialist = "General Physician"

        # update conversation memory
        self.chat_history.append((query, answer[:200]))  # truncate stored answer
        if len(self.chat_history) > MAX_CHAT_HISTORY:
            self.chat_history.pop(0)

        return {
            "answer": answer,
            "sources": sources,
            "confidence": round(confidence, 4),
            "icd_categories": icd_categories,
            "specialist": specialist,
        }


if __name__ == "__main__":
    # interactive loop for quick testing
    pipeline = RAGPipeline()

    print("Type 'quit' to exit\n")
    while True:
        query = input("You: ").strip()
        if not query:
            continue
        if query.lower() in ["quit", "exit", "q"]:
            break

        result = pipeline.get_answer(query)
        print(f"\nAssistant: {result['answer']}")
        if result["sources"]:
            print(f"Sources: {', '.join(result['sources'][:3])}")
        if result["specialist"]:
            print(f"Specialist: {result['specialist']}")
        print(f"Confidence: {result['confidence']:.3f}\n")
