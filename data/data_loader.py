import os
import pandas as pd
import xml.etree.ElementTree as ET

MEDQUAD_DIR = "data/raw/MedQuAD"
SYMPTOM_CSV = "data/raw/symptom_disease.csv"


def load_medquad(folder_path=MEDQUAD_DIR):
    """
    Walk through MedQuAD XML files and pull out question-answer pairs.
    Returns a list of dicts: {question, answer, source_url, category}
    """
    records = []

    if not os.path.exists(folder_path):
        print(f"[!] MedQuAD folder not found at {folder_path}")
        print("    Run download_datasets.py first")
        return records

    # MedQuAD has subfolders per category (e.g. 1_CancerGov_QA, 2_GARD_QA, ...)
    for root_dir, subdirs, files in os.walk(folder_path):
        for fname in files:
            if not fname.endswith(".xml"):
                continue

            fpath = os.path.join(root_dir, fname)
            try:
                tree = ET.parse(fpath)
                root = tree.getroot()

                # figure out the category from the folder name
                category = os.path.basename(root_dir)

                # each QAPair has Question and Answer children
                for qa in root.findall(".//QAPair"):
                    question_el = qa.find("Question")
                    answer_el = qa.find("Answer")

                    if question_el is None or answer_el is None:
                        continue

                    question = (question_el.text or "").strip()
                    answer = (answer_el.text or "").strip()

                    if not question or not answer:
                        continue

                    # try to grab the source URL if it's on the Document element
                    doc_el = root.find("Document")
                    source_url = ""
                    if doc_el is not None:
                        source_url = doc_el.get("source", "")

                    records.append({
                        "question": question,
                        "answer": answer,
                        "source_url": source_url,
                        "category": category,
                    })

            except ET.ParseError as e:
                print(f"  Skipping malformed XML: {fpath} ({e})")

    print(f"Loaded {len(records)} QA pairs from MedQuAD")
    return records


def load_symptom_csv(filepath=SYMPTOM_CSV):
    """
    Load the Kaggle symptom-disease CSV.
    The dataset has columns: Disease, Symptom_1 ... Symptom_17
    Returns a cleaned DataFrame.
    """
    if not os.path.exists(filepath):
        print(f"[!] Symptom CSV not found at {filepath}")
        return pd.DataFrame()

    df = pd.read_csv(filepath)

    # drop completely empty rows
    df.dropna(how="all", inplace=True)

    # strip whitespace from string columns
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.strip()

    # lowercase the disease name for consistency
    if "Disease" in df.columns:
        df["Disease"] = df["Disease"].str.lower()

    print(f"Loaded symptom CSV: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Diseases: {df['Disease'].nunique() if 'Disease' in df.columns else 'N/A'} unique")
    return df


if __name__ == "__main__":
    print("=== Loading MedQuAD ===")
    medquad = load_medquad()
    if medquad:
        print(f"Sample record:")
        sample = medquad[0]
        print(f"  Q: {sample['question'][:80]}...")
        print(f"  A: {sample['answer'][:80]}...")
        print(f"  Category: {sample['category']}")

    print("\n=== Loading Symptom CSV ===")
    symptom_df = load_symptom_csv()
    if not symptom_df.empty:
        print(symptom_df.head(3).to_string())
