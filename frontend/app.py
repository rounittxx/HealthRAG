import os
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
DEMO_MODE = os.getenv("HEALTHRAG_MODE", "demo").lower() != "live"

st.set_page_config(page_title="HealthRAG — Medical Q&A", layout="wide")

st.markdown("""<style>
.stApp { background: #f5f7fa; }
[data-testid="stSidebar"] { background: #1b2a4a; }
[data-testid="stSidebar"] * { color: #c0d4e8 !important; }
[data-testid="stSidebar"] h1 { color: #fff !important; font-size: 1.5rem; }
[data-testid="stSidebar"] .stButton button {
    background: #2c3e6b; color: #fff !important;
    border: 1px solid #3d5280; border-radius: 6px; width: 100%;
}
[data-testid="stChatMessage"] {
    background: #fff; border: 1px solid #dde3ec;
    border-radius: 10px; margin-bottom: 0.75rem;
}
.stButton button {
    background: #fff; border: 1px solid #c8d4e3;
    border-radius: 8px; font-size: 0.875rem; text-align: left;
}
footer, header, #MainMenu { visibility: hidden; }
</style>""", unsafe_allow_html=True)

DEMOS = {
    "diabetes": {
        "answer": """**What it is**
Type 2 diabetes is a condition where the body stops using insulin properly, causing blood sugar to rise over time. It develops gradually, often without obvious symptoms early on.

**Symptoms to watch for**
Increased thirst, frequent urination, unexplained tiredness, slow-healing wounds, blurred vision, and tingling in the hands or feet.

**When to get help urgently**
If you feel extremely drowsy or confused with high blood sugar, or shaky and sweaty with very low blood sugar — these need immediate attention.

**What actually helps**
Diet and exercise are genuinely the most powerful tools here. Cutting refined carbs, eating more whole foods, and getting 150 minutes of moderate activity a week can improve blood sugar dramatically — sometimes enough to reduce or avoid medication.

**When to see a doctor**
If you have any of the above symptoms, or risk factors like a family history or being overweight, ask your GP for a blood test. Early detection makes management much easier.

*This is general information only — always consult a healthcare professional about your situation.*""",
        "sources": ["https://www.nhs.uk/conditions/type-2-diabetes/", "https://pubmed.ncbi.nlm.nih.gov/?term=type+2+diabetes"],
        "confidence": 0.84, "icd_categories": ["Endocrine"], "specialist": "Endocrinologist",
    },
    "asthma": {
        "answer": """**What it is**
Asthma is a long-term condition where the airways get inflamed and narrowed, making breathing difficult. It varies a lot between people — some have occasional mild episodes, others have more frequent symptoms.

**Common symptoms**
Wheezing, breathlessness, chest tightness, and a persistent cough — often worse at night or in cold air.

**When to get help urgently**
Call emergency services if breathing becomes very difficult, lips go bluish, or a reliever inhaler isn't working after several puffs. A severe asthma attack is life-threatening.

**Day-to-day management**
Always carry your reliever inhaler. Know your triggers (cold air, dust, pollen, exercise) and try to manage them. A written asthma action plan from your GP or nurse is genuinely useful — most people don't have one but should.

**When to see a doctor**
If you're using your reliever more than twice a week, book a review. Your preventer inhaler dose or type might need adjusting.

*This is general information only — always consult a healthcare professional about your situation.*""",
        "sources": ["https://www.nhs.uk/conditions/asthma/", "https://pubmed.ncbi.nlm.nih.gov/?term=asthma+management"],
        "confidence": 0.81, "icd_categories": ["Respiratory"], "specialist": "Pulmonologist",
    },
    "heart": {
        "answer": """**What it is**
Heart disease most commonly refers to coronary artery disease — where arteries supplying the heart narrow due to fatty plaque build-up. This can cause chest pain (angina) or, if an artery becomes blocked, a heart attack.

**Symptoms**
Angina typically feels like pressure or tightness in the chest during exertion, relieved by rest. A heart attack causes more severe, persistent pain — often with sweating, nausea, and breathlessness. Women and diabetics may have less obvious symptoms.

**Emergency — act fast**
Call emergency services immediately for any unexplained chest pain that doesn't resolve quickly. Time matters enormously in a heart attack.

**What helps prevention**
Stopping smoking, controlling blood pressure and cholesterol, staying active, and eating well. A Mediterranean-style diet has the best evidence for heart health.

**When to see a doctor**
Chest discomfort with exertion, unexplained breathlessness, or strong family history of heart disease all warrant a GP visit sooner rather than later.

*This is general information only — always consult a healthcare professional about your situation.*""",
        "sources": ["https://www.nhs.uk/conditions/heart-attack/", "https://www.bhf.org.uk/"],
        "confidence": 0.82, "icd_categories": ["Cardiovascular"], "specialist": "Cardiologist",
    },
    "headache": {
        "answer": """**What it is**
Most headaches are either tension-type (a dull band of pressure, both sides) or migraine (throbbing, often one side, with nausea and light sensitivity). Migraines are a neurological condition, not just a bad headache.

**Migraine warning signs**
Some people get an "aura" before the headache — visual disturbances like zigzag lines or blind spots, tingling, or difficulty speaking. These are harmless but worth flagging to a doctor.

**When to seek emergency help**
A sudden, severe headache — "the worst of your life" — needs immediate medical attention. Same if accompanied by fever, stiff neck, confusion, weakness, or it follows a head injury.

**What helps**
For migraines: take pain relief early (triptans like sumatriptan work well), rest in a dark quiet room, stay hydrated. Keeping a headache diary to spot triggers (sleep, food, hormones, stress) is really useful.

**When to see a doctor**
If headaches are frequent, getting worse, or you're taking pain relief more than 10 days a month (that itself can cause rebound headaches).

*This is general information only — always consult a healthcare professional about your situation.*""",
        "sources": ["https://www.nhs.uk/conditions/headaches/", "https://www.migrainetrust.org/"],
        "confidence": 0.78, "icd_categories": ["Neurological"], "specialist": "Neurologist",
    },
    "blood pressure": {
        "answer": """**What it is**
High blood pressure (hypertension) is when blood pushes too hard against artery walls over time. It usually causes no symptoms — which is exactly what makes it dangerous. Uncontrolled, it significantly raises the risk of stroke, heart attack, and kidney disease.

**What counts as high**
Consistently above 140/90 mmHg in clinic (135/85 at home). A single high reading doesn't mean you have hypertension — it needs to be confirmed over time.

**What genuinely brings it down**
Reducing salt intake makes the biggest dietary difference. Regular aerobic exercise, losing weight if overweight, limiting alcohol, and stopping smoking all help meaningfully. The DASH diet has strong evidence behind it.

**If you're on medication**
Take it consistently even when you feel fine — the whole point is preventing silent damage. Never stop without talking to your doctor first.

**When to see a doctor**
Get your blood pressure checked regularly if you're over 40, have a family history, or are overweight. If it's very high (above 180/120), contact your GP or urgent care the same day.

*This is general information only — always consult a healthcare professional about your situation.*""",
        "sources": ["https://www.nhs.uk/conditions/high-blood-pressure-hypertension/", "https://www.bhf.org.uk/"],
        "confidence": 0.85, "icd_categories": ["Cardiovascular"], "specialist": "Cardiologist",
    },
    "depression": {
        "answer": """**What it is**
Depression is a medical condition — not a mood or a weakness. It causes persistent low mood, loss of enjoyment, fatigue, and difficulty with everyday tasks for weeks or months at a time. Brain chemistry changes are involved and it responds to treatment.

**Common signs**
Feeling empty or hopeless most days, no interest in things you used to enjoy, exhaustion, poor sleep, difficulty concentrating, and sometimes thoughts of self-harm or death.

**If someone is in crisis**
Please don't wait. In the UK call Samaritans on 116 123 (free, 24/7) or go to A&E. In the US call or text 988.

**What actually works**
CBT (cognitive behavioural therapy) and antidepressants both have solid evidence, and combining them is often more effective than either alone. Regular exercise has surprisingly strong evidence too — comparable to medication in mild-to-moderate cases.

**First step**
Talk to your GP. Depression is very treatable, especially when caught early. Reaching out is harder than it sounds but it's the most important thing.

*This is general information only — always consult a healthcare professional about your situation.*""",
        "sources": ["https://www.nhs.uk/mental-health/conditions/depression/", "https://www.mind.org.uk/"],
        "confidence": 0.83, "icd_categories": ["Mental Health"], "specialist": "Psychiatrist",
    },
    "anxiety": {
        "answer": """**What it is**
Anxiety disorders go beyond normal worry. Generalised anxiety disorder (GAD) involves persistent, hard-to-control worry about many different things — not just one specific situation. It often comes with physical symptoms like muscle tension, racing heart, and poor sleep.

**Symptoms**
Excessive worry that's difficult to switch off, irritability, restlessness, difficulty concentrating, fatigue, and physical symptoms like headaches, nausea, and sweating.

**Things that help right now**
Slow diaphragmatic breathing (breathe in for 4 counts, out for 6) activates the body's calm response. Grounding techniques — naming 5 things you can see, 4 you can touch — help interrupt anxious spirals. Regular exercise is genuinely one of the best anxiolytics available.

**Longer-term**
CBT is the most evidence-backed psychological treatment for anxiety. SSRIs (like sertraline) are effective medical options. Most people do well with a combination of both.

**When to see someone**
If anxiety is stopping you from doing things you want or need to do, it's worth talking to your GP. You don't have to feel this way indefinitely.

*This is general information only — always consult a healthcare professional about your situation.*""",
        "sources": ["https://www.nhs.uk/mental-health/conditions/generalised-anxiety-disorder/", "https://www.anxietyuk.org.uk/"],
        "confidence": 0.80, "icd_categories": ["Mental Health"], "specialist": "Psychiatrist",
    },
    "back pain": {
        "answer": """**The reassuring bit first**
Most lower back pain — over 90% — has no serious cause and resolves within 4-6 weeks. The spine is robust and the pain usually comes from muscles, ligaments, or mild disc changes rather than structural damage.

**What makes it worse**
Bed rest. Counterintuitively, staying still prolongs recovery. Keeping moving gently, even when it's uncomfortable, is the single best thing you can do.

**Red flags — go to A&E**
Loss of bladder or bowel control, numbness in the inner thigh, or progressive leg weakness alongside back pain need immediate assessment. These are rare but serious.

**What actually helps**
Heat packs, gentle walking, paracetamol or ibuprofen for pain, and keeping your normal routine as much as possible. Anxiety and low mood are among the strongest predictors of pain becoming chronic — addressing them matters.

**When to see a doctor**
If pain isn't improving after 4-6 weeks, is getting progressively worse, or comes with unexplained weight loss or fever.

*This is general information only — always consult a healthcare professional about your situation.*""",
        "sources": ["https://www.nhs.uk/conditions/back-pain/", "https://cks.nice.org.uk/topics/back-pain-low-without-radiculopathy/"],
        "confidence": 0.77, "icd_categories": ["Musculoskeletal"], "specialist": "Physiotherapist",
    },
    "default": {
        "answer": """I couldn't find a reliable match in my knowledge base for that question. This sometimes happens with very specific symptoms or unusual phrasing.

For general health information, NHS.uk and MedlinePlus are good places to start — both are clear and evidence-based.

For anything that's worrying you or affecting your daily life, please speak to your GP. They can properly assess your situation, arrange tests if needed, and refer you to the right specialist.

If it's urgent, don't wait for an appointment — contact urgent care or go to your nearest emergency department.

*This is general information only — always consult a healthcare professional about your situation.*""",
        "sources": [], "confidence": 0.38, "icd_categories": [], "specialist": "General Physician",
    },
}

SAMPLES = [
    "What are the symptoms of type 2 diabetes?",
    "How is asthma managed day to day?",
    "What causes high blood pressure?",
    "What is depression and how is it treated?",
    "How do I manage lower back pain?",
    "What are the warning signs of a heart attack?",
]


def get_demo(query):
    q = query.lower()
    for key in DEMOS:
        if key != "default" and key in q:
            return DEMOS[key]
    return DEMOS["default"]


def confidence_tag(score):
    if score >= 0.7:
        return "High confidence", "normal"
    elif score >= 0.45:
        return "Moderate confidence", "warning"
    return "Low confidence", "warning"


def ask(query, history):
    if DEMO_MODE:
        return get_demo(query)
    try:
        r = requests.post(f"{API_BASE_URL}/ask", json={"query": query, "history": history}, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        return {"answer": "Could not reach the backend. Make sure the API server is running.", "sources": [], "confidence": 0.0, "icd_categories": [], "specialist": None}
    except Exception as e:
        return {"answer": f"Something went wrong: {e}", "sources": [], "confidence": 0.0, "icd_categories": [], "specialist": None}


if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []

# sidebar
with st.sidebar:
    st.title("HealthRAG")
    st.caption("Medical Q&A — powered by BioBERT and FAISS")
    st.markdown("---")
    st.markdown("Ask about symptoms, conditions, or treatments. Answers come from NHS and PubMed literature.")
    st.markdown("---")
    st.caption("General information only. Not a substitute for medical advice.")
    if DEMO_MODE:
        st.info("Demo mode — set HEALTHRAG_MODE=live for real AI answers.")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

# main
st.markdown("## Medical Q&A Assistant")
st.caption("Ask a health question in plain language. Answers are grounded in published medical literature.")

# render chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "meta" in msg:
            m = msg["meta"]
            label, kind = confidence_tag(m.get("confidence", 0))
            cols = st.columns([2, 2, 3])
            cols[0].caption(f"{label} ({m.get('confidence', 0):.0%})")
            if m.get("specialist"):
                cols[1].caption(f"See: {m['specialist']}")
            if m.get("icd_categories"):
                cols[2].caption(" · ".join(m["icd_categories"]))
            if m.get("sources"):
                with st.expander("Sources"):
                    for s in m["sources"]:
                        st.markdown(f"- [{s}]({s})")

# welcome state
if not st.session_state.messages:
    st.markdown("**Not sure what to ask? Try one of these:**")
    cols = st.columns(2)
    for i, s in enumerate(SAMPLES):
        if cols[i % 2].button(s, key=f"s{i}", use_container_width=True):
            st.session_state._prefill = s
            st.rerun()

# input
prefill = getattr(st.session_state, "_prefill", None)
if prefill:
    st.session_state._prefill = None
    prompt = prefill
else:
    prompt = st.chat_input("Ask a health question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Looking through the medical literature..."):
            result = ask(prompt, st.session_state.history)
        answer = result.get("answer", "No answer received.")
        st.markdown(answer)

        label, _ = confidence_tag(result.get("confidence", 0))
        cols = st.columns([2, 2, 3])
        cols[0].caption(f"{label} ({result.get('confidence', 0):.0%})")
        if result.get("specialist"):
            cols[1].caption(f"See: {result['specialist']}")
        if result.get("icd_categories"):
            cols[2].caption(" · ".join(result["icd_categories"]))
        if result.get("sources"):
            with st.expander("Sources"):
                for s in result["sources"]:
                    st.markdown(f"- [{s}]({s})")

    st.session_state.messages.append({"role": "assistant", "content": answer, "meta": result})
    st.session_state.history.append([prompt, answer[:200]])
    if len(st.session_state.history) > 4:
        st.session_state.history.pop(0)
