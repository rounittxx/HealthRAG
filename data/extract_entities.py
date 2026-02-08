import json
import os

# scispacy gives us biomedical NER without fine-tuning anything ourselves
# Install: pip install scispacy
# Then: pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.3/en_core_sci_sm-0.5.3.tar.gz

try:
    import spacy
    nlp = spacy.load("en_core_sci_sm")
    print("Loaded en_core_sci_sm model")
except OSError:
    print("[!] en_core_sci_sm not found. Run:")
    print("    pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.3/en_core_sci_sm-0.5.3.tar.gz")
    nlp = None


def extract_entities(text):
    """
    Run spaCy NER on medical text.
    Returns list of (entity_text, label) tuples.
    """
    if nlp is None:
        return []

    doc = nlp(text[:1000])  # cap at 1000 chars to avoid slow processing
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


def process_dataset(records):
    """
    Adds an 'entities' field to each record.
    This is used to enrich the RAG knowledge base with structured medical terms.
    """
    if nlp is None:
        print("[!] spaCy model not loaded, skipping entity extraction")
        return records

    print(f"Extracting entities from {len(records)} records...")
    for i, rec in enumerate(records):
        text = rec.get("text", rec.get("answer", ""))
        rec["entities"] = extract_entities(text)

        if i % 1000 == 0:
            print(f"  Processed {i}/{len(records)} records")

    return records


def save_with_entities(records, output_path="data/processed/chunks_with_entities.json"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(records, f, indent=2)
    print(f"Saved {len(records)} records with entities to {output_path}")


if __name__ == "__main__":
    # load cleaned chunks from Phase 1
    chunks_path = "data/processed/cleaned_chunks.json"
    if not os.path.exists(chunks_path):
        print(f"[!] Run clean_text.py first to generate {chunks_path}")
    else:
        with open(chunks_path) as f:
            chunks = json.load(f)

        chunks = process_dataset(chunks[:100])  # test on first 100

        print("\nFirst 5 records with entities:")
        for rec in chunks[:5]:
            print(f"  Text: {rec['text'][:60]}...")
            print(f"  Entities: {rec['entities'][:3]}")
            print()
