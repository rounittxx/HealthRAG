"""
Streamlit chat frontend for HealthRAG.
Supports two modes:
  - DEMO mode (HF Spaces): uses a mock response so it runs without the FastAPI backend
  - LIVE mode: connects to the real FastAPI backend at API_BASE_URL

Set env var HEALTHRAG_MODE=live to enable live mode.
# st.session_state persists chat history across reruns — I spent an hour figuring this out
"""

import os
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
DEMO_MODE = os.getenv("HEALTHRAG_MODE", "demo").lower() != "live"

st.set_page_config(
    page_title="HealthRAG — Medical Q&A",
    page_icon="🩺",
    layout="wide",
)

with st.sidebar:
    st.title("🩺 HealthRAG")
    st.markdown("""
        **AI Medical Q&A Assistant**

        Ask about symptoms, conditions, medications, or treatments.
        Answers are grounded in PubMed and NHS medical literature.

        ---
        ⚠️ **Disclaimer**
        General health information only — NOT a substitute for
        professional medical advice. Always consult a qualified doctor.
        ---
    """)
    if DEMO_MODE:
        st.info("🎮 **Demo Mode** — illustrative responses.\nSet `HEALTHRAG_MODE=live` + deploy backend for real AI answers.")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()
    st.markdown("[View on GitHub](https://github.com/rounittxx/HealthRAG)")
    st.caption("Powered by BioBERT · FAISS · LangChain")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

DEMO_RESPONSES = {
    "diabetes": {
        "answer": "Type 2 diabetes is a chronic metabolic condition where the body doesn't use insulin effectively, causing elevated blood glucose. Symptoms include increased thirst, frequent urination, fatigue, and slow-healing wounds. Management typically involves lifestyle changes, metformin, and sometimes insulin.\n\n---\n⚠️ This is general information only — not a substitute for medical advice.",
        "sources": ["https://www.ncbi.nlm.nih.gov/pubmed/diabetes-type2", "https://www.nhs.uk/conditions/type-2-diabetes/"],
        "confidence": 0.81, "icd_categories": ["Endocrine"], "specialist": "Endocrinologist",
    },
    "asthma": {
        "answer": "Asthma is a chronic respiratory condition causing airway inflammation and narrowing, leading to wheezing, breathlessness, and coughing. Triggers include allergens, cold air, and exercise. Treatment involves controller inhalers (corticosteroids) and reliever inhalers (bronchodilators).\n\n---\n⚠️ This is general information only — not a substitute for medical advice.",
        "sources": ["https://www.ncbi.nlm.nih.gov/pubmed/asthma", "https://www.nhs.uk/conditions/asthma/"],
        "confidence": 0.79, "icd_categories": ["Respiratory"], "specialist": "Pulmonologist",
    },
    "heart": {
        "answer": "Heart disease encompasses conditions affecting the heart. Heart attack symptoms include chest pain, arm/jaw pain, shortness of breath, and sweating. Risk factors include hypertension, high cholesterol, smoking, and diabetes. If you suspect a heart attack, call emergency services immediately.\n\n---\n⚠️ This is general information only — not a substitute for medical advice.",
        "sources": ["https://www.ncbi.nlm.nih.gov/pubmed/cardiovascular", "https://www.nhs.uk/conditions/heart-attack/"],
        "confidence": 0.77, "icd_categories": ["Cardiovascular"], "specialist": "Cardiologist",
    },
    "headache": {
        "answer": "Headaches range from tension-type to migraines. Migraines cause severe throbbing pain, often one-sided, with nausea and light sensitivity. Most headaches respond to rest, hydration, and OTC pain relief. Persistent or severe headaches need medical evaluation.\n\n---\n⚠️ This is general information only — not a substitute for medical advice.",
        "sources": ["https://www.ncbi.nlm.nih.gov/pubmed/migraine", "https://www.nhs.uk/conditions/headaches/"],
        "confidence": 0.74, "icd_categories": ["Neurological"], "specialist": "Neurologist",
    },
    "blood pressure": {
        "answer": "Hypertension (high blood pressure) is when the force of blood against artery walls is consistently too high. Often symptom-free, it increases risk of heart disease, stroke, and kidney problems. Managed through lifestyle changes (diet, exercise, less salt) and medications like ACE inhibitors or calcium channel blockers.\n\n---\n⚠️ This is general information only — not a substitute for medical advice.",
        "sources": ["https://www.ncbi.nlm.nih.gov/pubmed/hypertension", "https://www.nhs.uk/conditions/high-blood-pressure/"],
        "confidence": 0.82, "icd_categories": ["Cardiovascular"], "specialist": "Cardiologist",
    },
    "default": {
        "answer": "Based on the medical literature in my knowledge base, this topic requires careful evaluation. Symptoms vary significantly between individuals and proper diagnosis needs a physical examination and possibly diagnostic tests. I recommend consulting a healthcare professional for personalised advice.\n\n---\n⚠️ This is general information only — not a substitute for medical advice.",
        "sources": ["https://www.ncbi.nlm.nih.gov/pubmed/", "https://www.nhs.uk/conditions/"],
        "confidence": 0.58, "icd_categories": [], "specialist": "General Physician",
    },
}


def get_demo_response(query):
    q = query.lower()
    for keyword, response in DEMO_RESPONSES.items():
        if keyword != "default" and keyword in q:
            return response
    return DEMO_RESPONSES["default"]


def confidence_badge(score):
    if score >= 0.7:
        return f"🟢 High confidence ({score:.2f})"
    elif score >= 0.45:
        return f"🟡 Moderate confidence ({score:.2f})"
    else:
        return f"🔴 Low confidence ({score:.2f})"


def ask_api(query, history):
    if DEMO_MODE:
        return get_demo_response(query)
    try:
        resp = requests.post(f"{API_BASE_URL}/ask", json={"query": query, "history": history}, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        return {"answer": "⚠️ Could not connect to the HealthRAG API. Make sure the backend is running.", "sources": [], "confidence": 0.0, "icd_categories": [], "specialist": None}
    except Exception as e:
        return {"answer": f"⚠️ Error: {str(e)}", "sources": [], "confidence": 0.0, "icd_categories": [], "specialist": None}


st.title("❤️ HealthRAG — Medical Q&A Assistant")
st.caption("Evidence-based answers from PubMed and NHS medical literature")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "meta" in msg:
            meta = msg["meta"]
            st.caption(confidence_badge(meta.get("confidence", 0)))
            if meta.get("specialist"):
                st.info(f"🏥 Recommended specialist: **{meta['specialist']}**")
            if meta.get("icd_categories"):
                st.caption(f"ICD-10 categories: {', '.join(meta['icd_categories'])}")
            if meta.get("sources"):
                with st.expander("📚 Sources"):
                    for src in meta["sources"]:
                        st.markdown(f"- [{src}]({src})")

if not st.session_state.messages:
    st.markdown("**Try asking:**")
    cols = st.columns(3)
    samples = ["What are the symptoms of diabetes?", "How is asthma treated?", "What causes high blood pressure?"]
    for col, s in zip(cols, samples):
        if col.button(s, use_container_width=True):
            st.session_state._prefill = s
            st.rerun()

prefill = getattr(st.session_state, "_prefill", None)
if prefill:
    st.session_state._prefill = None
    prompt = prefill
else:
    prompt = st.chat_input("Ask a health question, e.g. 'What are the symptoms of diabetes?'")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Searching medical literature..."):
            result = ask_api(prompt, st.session_state.chat_history)
        answer = result.get("answer", "No answer received.")
        st.markdown(answer)
        st.caption(confidence_badge(result.get("confidence", 0)))
        if result.get("specialist"):
            st.info(f"🏥 Recommended specialist: **{result['specialist']}**")
        if result.get("icd_categories"):
            st.caption(f"ICD-10 categories: {', '.join(result['icd_categories'])}")
        if result.get("sources"):
            with st.expander("📚 Sources"):
                for src in result["sources"]:
                    st.markdown(f"- [{src}]({src})")
    st.session_state.messages.append({"role": "assistant", "content": answer, "meta": result})
    st.session_state.chat_history.append([prompt, answer[:200]])
    if len(st.session_state.chat_history) > 4:
        st.session_state.chat_history.pop(0)
