"""
Unit tests for all pure-Python modules — no ML packages needed.
These run in CI without GPU/heavy deps.
Run with: pytest tests/test_unit.py -v
"""

import sys
import os
import unittest.mock as mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ── config ────────────────────────────────────────────────────────────────────

def test_config_values():
    import config
    assert config.CHUNK_SIZE == 512
    assert config.OVERLAP == 50
    assert config.CONFIDENCE_THRESHOLD == 0.45
    assert config.TOP_K_RETRIEVAL == 5
    assert config.MAX_CHAT_HISTORY == 4
    assert isinstance(config.USE_LOCAL_LLM, bool)


# ── clean_text ────────────────────────────────────────────────────────────────

def test_clean_strips_html():
    from data.clean_text import clean_medical_text
    raw = "<p>Diabetes <b>mellitus</b> type-2</p>"
    cleaned = clean_medical_text(raw)
    assert "<p>" not in cleaned
    assert "<b>" not in cleaned
    assert "diabetes" in cleaned


def test_clean_decodes_html_entities():
    from data.clean_text import clean_medical_text
    raw = "symptoms &amp; signs of &lt;condition&gt;"
    cleaned = clean_medical_text(raw)
    assert "&amp;" not in cleaned
    assert "&lt;" not in cleaned
    assert "symptoms" in cleaned


def test_clean_collapses_whitespace():
    from data.clean_text import clean_medical_text
    raw = "too    many   spaces\n\nand newlines"
    cleaned = clean_medical_text(raw)
    assert "  " not in cleaned


def test_clean_keeps_medical_punctuation():
    from data.clean_text import clean_medical_text
    raw = "beta-blocker (HbA1c) 7.5% result"
    cleaned = clean_medical_text(raw)
    assert "beta-blocker" in cleaned
    assert "(" in cleaned


def test_clean_empty_input():
    from data.clean_text import clean_medical_text
    assert clean_medical_text("") == ""
    assert clean_medical_text(None) == ""


def test_chunk_short_text_no_split():
    from data.clean_text import chunk_text
    short = " ".join(["word"] * 100)
    chunks = chunk_text(short, chunk_size=512, overlap=50)
    assert len(chunks) == 1


def test_chunk_long_text_splits():
    from data.clean_text import chunk_text
    long = " ".join(["word"] * 600)
    chunks = chunk_text(long, chunk_size=512, overlap=50)
    assert len(chunks) == 2


def test_chunk_overlap_retained():
    from data.clean_text import chunk_text
    # build text with unique words so we can check overlap
    words = [f"w{i}" for i in range(600)]
    text = " ".join(words)
    chunks = chunk_text(text, chunk_size=512, overlap=50)
    # last 50 words of chunk 0 should appear at start of chunk 1
    chunk0_words = set(chunks[0].split())
    chunk1_words = set(chunks[1].split())
    overlap = chunk0_words & chunk1_words
    assert len(overlap) >= 45  # at least 45 words in common (some tolerance)


def test_remove_duplicates():
    from data.clean_text import remove_duplicates
    records = [
        {"question": "What is diabetes?"},
        {"question": "What is diabetes?"},   # exact duplicate
        {"question": "what is diabetes?"},   # lowercase duplicate
        {"question": "What is asthma?"},
    ]
    unique = remove_duplicates(records)
    assert len(unique) == 2


# ── prompt templates ──────────────────────────────────────────────────────────

def test_medical_qa_template_has_placeholders():
    from rag.prompt_templates import MEDICAL_QA_TEMPLATE
    assert "{context}" in MEDICAL_QA_TEMPLATE
    assert "{question}" in MEDICAL_QA_TEMPLATE


def test_medical_qa_template_has_safety_rules():
    from rag.prompt_templates import MEDICAL_QA_TEMPLATE
    assert "ONLY from the context" in MEDICAL_QA_TEMPLATE
    assert "not a substitute" in MEDICAL_QA_TEMPLATE.lower()
    assert "consult" in MEDICAL_QA_TEMPLATE.lower()


def test_medical_qa_template_fills_correctly():
    from rag.prompt_templates import MEDICAL_QA_TEMPLATE
    prompt = MEDICAL_QA_TEMPLATE.format(
        context="Diabetes is a metabolic disease.",
        question="What is diabetes?"
    )
    assert "Diabetes is a metabolic disease." in prompt
    assert "What is diabetes?" in prompt


def test_safety_check_template():
    from rag.prompt_templates import SAFETY_CHECK_TEMPLATE
    assert "{question}" in SAFETY_CHECK_TEMPLATE
    filled = SAFETY_CHECK_TEMPLATE.format(question="write a poem")
    assert "write a poem" in filled


def test_low_confidence_response_has_doctor_advice():
    from rag.prompt_templates import LOW_CONFIDENCE_RESPONSE
    assert "doctor" in LOW_CONFIDENCE_RESPONSE.lower() or "healthcare" in LOW_CONFIDENCE_RESPONSE.lower()


# ── classifier disease mappings ───────────────────────────────────────────────

def test_disease_to_icd10_has_key_diseases():
    # patch sklearn so module loads cleanly
    with mock.patch.dict("sys.modules", {"sklearn": mock.MagicMock(),
                                          "sklearn.model_selection": mock.MagicMock()}):
        from classifier.prepare_classifier_data import DISEASE_TO_ICD10, ALL_CATEGORIES

    assert "diabetes" in DISEASE_TO_ICD10
    assert DISEASE_TO_ICD10["diabetes"] == "Endocrine"
    assert "pneumonia" in DISEASE_TO_ICD10
    assert DISEASE_TO_ICD10["pneumonia"] == "Respiratory"
    assert "hypertension" in DISEASE_TO_ICD10
    assert DISEASE_TO_ICD10["hypertension"] == "Cardiovascular"
    assert "depression" in DISEASE_TO_ICD10
    assert DISEASE_TO_ICD10["depression"] == "Mental Health"
    assert len(ALL_CATEGORIES) >= 10


def test_label_vector_is_one_hot():
    with mock.patch.dict("sys.modules", {"sklearn": mock.MagicMock(),
                                          "sklearn.model_selection": mock.MagicMock()}):
        from classifier.prepare_classifier_data import make_label_vector, ALL_CATEGORIES

    for cat in ALL_CATEGORIES:
        vec = make_label_vector(cat)
        assert len(vec) == len(ALL_CATEGORIES)
        assert sum(vec) == 1
        assert vec[ALL_CATEGORIES.index(cat)] == 1


# ── specialist router ─────────────────────────────────────────────────────────

def test_all_icd_categories_have_specialist():
    with mock.patch.dict("sys.modules", {"classifier.inference": mock.MagicMock()}):
        from classifier.specialist_router import ICD_TO_SPECIALIST

    expected_cats = ["Endocrine", "Respiratory", "Cardiovascular", "Neurological",
                     "Gastrointestinal", "Musculoskeletal", "Dermatological",
                     "Infectious", "Mental Health", "Hematological", "Renal"]
    for cat in expected_cats:
        assert cat in ICD_TO_SPECIALIST, f"{cat} missing from ICD_TO_SPECIALIST"


def test_recommend_specialist_correct_routing():
    with mock.patch.dict("sys.modules", {"classifier.inference": mock.MagicMock()}):
        from classifier.specialist_router import recommend_specialist

    cases = [
        ([("Respiratory", 0.85)], "Pulmonologist"),
        ([("Cardiovascular", 0.72)], "Cardiologist"),
        ([("Neurological", 0.91)], "Neurologist"),
        ([("Endocrine", 0.80)], "Endocrinologist"),
        ([("Mental Health", 0.75)], "Psychiatrist"),
        ([("Unknown", 0.0)], "General Physician"),
    ]
    for icd_input, expected in cases:
        specialist, reason = recommend_specialist(icd_input)
        assert specialist == expected, f"Expected {expected} for {icd_input}, got {specialist}"
        assert isinstance(reason, str) and len(reason) > 5


def test_low_confidence_adds_gp_note():
    with mock.patch.dict("sys.modules", {"classifier.inference": mock.MagicMock()}):
        from classifier.specialist_router import recommend_specialist

    specialist, reason = recommend_specialist([("Respiratory", 0.25)])
    # either specialist is GP, or reason mentions GP
    assert "General Physician" in reason or specialist == "General Physician"


def test_empty_categories_returns_gp():
    with mock.patch.dict("sys.modules", {"classifier.inference": mock.MagicMock()}):
        from classifier.specialist_router import recommend_specialist

    specialist, reason = recommend_specialist([])
    assert "General Physician" in specialist or "General Physician" in reason


# ── api schemas ───────────────────────────────────────────────────────────────

def test_schema_classes_exist():
    """Verify schema classes can be inspected without pydantic installed."""
    import ast
    src = open(os.path.join(os.path.dirname(__file__), "../api/schemas.py")).read()
    tree = ast.parse(src)
    class_names = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    assert "AskRequest" in class_names
    assert "AskResponse" in class_names
    assert "ClassifyRequest" in class_names
    assert "ClassifyResponse" in class_names
    assert "HealthResponse" in class_names


# ── api endpoints defined ─────────────────────────────────────────────────────

def test_api_has_all_endpoints():
    src = open(os.path.join(os.path.dirname(__file__), "../api/main.py")).read()
    assert '"/ask"' in src or "'/ask'" in src
    assert '"/classify"' in src or "'/classify'" in src
    assert '"/health"' in src or "'/health'" in src
    assert "CORSMiddleware" in src
    assert "lifespan" in src


# ── rag pipeline structure ────────────────────────────────────────────────────

def test_rag_pipeline_has_required_methods():
    src = open(os.path.join(os.path.dirname(__file__), "../rag/rag_pipeline.py")).read()
    assert "class RAGPipeline" in src
    assert "def get_answer" in src
    assert "def is_medical_query" in src
    assert "CONFIDENCE_THRESHOLD" in src
    assert "hybrid_search" in src
    assert "chat_history" in src


# ── retrieval engine structure ────────────────────────────────────────────────

def test_retrieval_engine_hybrid_weights_sum_to_one():
    import ast
    src = open(os.path.join(os.path.dirname(__file__), "../retrieval/retrieval_engine.py")).read()
    # extract DENSE_WEIGHT and BM25_WEIGHT values
    tree = ast.parse(src)
    weights = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in ("DENSE_WEIGHT", "BM25_WEIGHT"):
                    weights[t.id] = ast.literal_eval(node.value)

    assert "DENSE_WEIGHT" in weights
    assert "BM25_WEIGHT" in weights
    assert abs(weights["DENSE_WEIGHT"] + weights["BM25_WEIGHT"] - 1.0) < 0.001, \
        f"Weights should sum to 1.0, got {weights['DENSE_WEIGHT']} + {weights['BM25_WEIGHT']}"


def test_retrieval_engine_has_all_functions():
    src = open(os.path.join(os.path.dirname(__file__), "../retrieval/retrieval_engine.py")).read()
    assert "def hybrid_search" in src
    assert "def embed_query" in src
    assert "def dense_search" in src
    assert "def load_resources" in src
