import os
import sys
import pandas as pd
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MEDQUAD_DIR = "data/raw/MedQuAD"
SYMPTOM_CSV = "data/raw/symptom_disease.csv"


def load_medquad(folder_path=MEDQUAD_DIR):
    records = []
    if not os.path.exists(folder_path):
        print(f"[!] MedQuAD not found at {folder_path} — run download_datasets.py first")
        return records

    for root_dir, _, files in os.walk(folder_path):
        for fname in files:
            if not fname.endswith(".xml"):
                continue
            fpath = os.path.join(root_dir, fname)
            try:
                tree = ET.parse(fpath)
                root = tree.getroot()
                category = os.path.basename(root_dir)
                doc_el = root.find("Document")
                source_url = doc_el.get("source", "") if doc_el is not None else ""
                for qa in root.findall(".//QAPair"):
                    q = (qa.findtext("Question") or "").strip()
                    a = (qa.findtext("Answer") or "").strip()
                    if q and a:
                        records.append({"question": q, "answer": a, "source_url": source_url, "category": category})
            except ET.ParseError as e:
                print(f"  Skipping {fpath}: {e}")

    print(f"Loaded {len(records)} QA pairs from MedQuAD")
    return records


def load_symptom_csv(filepath=SYMPTOM_CSV):
    if not os.path.exists(filepath):
        print(f"[!] Symptom CSV not found at {filepath}")
        return pd.DataFrame()

    df = pd.read_csv(filepath).dropna(how="all")
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
    if "Disease" in df.columns:
        df["Disease"] = df["Disease"].str.lower()

    print(f"Loaded symptom CSV: {df.shape[0]} rows, {df['Disease'].nunique()} diseases")
    return df


def load_extended_kb():
    try:
        from extended_medical_kb import get_all_documents
        docs = get_all_documents()
        print(f"Loaded {len(docs)} documents from extended knowledge base")
        return docs
    except ImportError as e:
        print(f"[!] Could not load extended knowledge base: {e}")
        return []


def load_all_sources():
    records = load_medquad() + load_extended_kb()
    print(f"Total: {len(records)} records")
    return records


if __name__ == "__main__":
    load_all_sources()
