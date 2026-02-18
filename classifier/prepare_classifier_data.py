"""
Prepares the Kaggle symptom-disease CSV for BioBERT multi-label classification.
Maps diseases to ICD-10 categories and creates train/val/test splits.
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split

SYMPTOM_CSV = "data/raw/symptom_disease.csv"
OUTPUT_DIR = "data/processed/classifier"

# I mapped diseases to ICD-10 categories manually — took an afternoon but worth it
# This covers the most common diseases in the Kaggle dataset
DISEASE_TO_ICD10 = {
    # Endocrine
    "diabetes": "Endocrine",
    "type 1 diabetes": "Endocrine",
    "type 2 diabetes": "Endocrine",
    "hypothyroidism": "Endocrine",
    "hyperthyroidism": "Endocrine",
    "hypoglycemia": "Endocrine",
    "obesity": "Endocrine",
    # Respiratory
    "pneumonia": "Respiratory",
    "tuberculosis": "Respiratory",
    "asthma": "Respiratory",
    "bronchial asthma": "Respiratory",
    "bronchitis": "Respiratory",
    "copd": "Respiratory",
    "common cold": "Respiratory",
    "influenza": "Respiratory",
    # Cardiovascular
    "hypertension": "Cardiovascular",
    "heart attack": "Cardiovascular",
    "heart failure": "Cardiovascular",
    "coronary artery disease": "Cardiovascular",
    "arrhythmia": "Cardiovascular",
    "varicose veins": "Cardiovascular",
    # Neurological
    "migraine": "Neurological",
    "epilepsy": "Neurological",
    "multiple sclerosis": "Neurological",
    "parkinson's disease": "Neurological",
    "alzheimer's disease": "Neurological",
    "cervical spondylosis": "Neurological",
    # Gastrointestinal
    "gastroenteritis": "Gastrointestinal",
    "peptic ulcer disease": "Gastrointestinal",
    "gerd": "Gastrointestinal",
    "hepatitis a": "Gastrointestinal",
    "hepatitis b": "Gastrointestinal",
    "hepatitis c": "Gastrointestinal",
    "hepatitis d": "Gastrointestinal",
    "hepatitis e": "Gastrointestinal",
    "jaundice": "Gastrointestinal",
    "chronic cholestasis": "Gastrointestinal",
    # Musculoskeletal
    "osteoarthritis": "Musculoskeletal",
    "rheumatoid arthritis": "Musculoskeletal",
    "arthritis": "Musculoskeletal",
    "fibromyalgia": "Musculoskeletal",
    "gout": "Musculoskeletal",
    # Dermatological
    "psoriasis": "Dermatological",
    "eczema": "Dermatological",
    "acne": "Dermatological",
    "fungal infection": "Dermatological",
    "chicken pox": "Dermatological",
    "impetigo": "Dermatological",
    "shingles": "Dermatological",
    # Infectious
    "malaria": "Infectious",
    "dengue": "Infectious",
    "typhoid": "Infectious",
    "aids": "Infectious",
    "urinary tract infection": "Infectious",
    # Mental Health
    "depression": "Mental Health",
    "anxiety": "Mental Health",
    "bipolar disorder": "Mental Health",
    # Hematological
    "anemia": "Hematological",
    "thalassemia": "Hematological",
    "thrombocytopenia": "Hematological",
    # Renal/Urological
    "chronic kidney disease": "Renal",
    "kidney stones": "Renal",
    "urinary tract infection": "Renal",
}

# all unique ICD-10 categories in our mapping
ALL_CATEGORIES = sorted(set(DISEASE_TO_ICD10.values()))


def reshape_symptom_df(df):
    """
    Kaggle CSV has Disease + Symptom_1 ... Symptom_17 columns.
    Combine all symptoms into a single text string per row.
    """
    symptom_cols = [c for c in df.columns if c.startswith("Symptom")]

    rows = []
    for _, row in df.iterrows():
        disease = str(row.get("Disease", "")).strip().lower()
        symptoms = [
            str(row[col]).strip().replace("_", " ")
            for col in symptom_cols
            if pd.notna(row[col]) and str(row[col]).strip() not in ["", "nan"]
        ]
        if not symptoms:
            continue

        symptom_text = ", ".join(symptoms)
        icd_category = DISEASE_TO_ICD10.get(disease, "Other")

        rows.append({
            "disease": disease,
            "symptom_text": symptom_text,
            "icd_category": icd_category,
        })

    return pd.DataFrame(rows)


def make_label_vector(icd_category, categories=ALL_CATEGORIES):
    """Create a binary label vector for multi-label classification."""
    return [1 if cat == icd_category else 0 for cat in categories]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(SYMPTOM_CSV):
        print(f"[!] Symptom CSV not found at {SYMPTOM_CSV}")
        print("    Download from Kaggle and place at data/raw/symptom_disease.csv")
        return

    print("Loading symptom CSV...")
    df = pd.read_csv(SYMPTOM_CSV)
    print(f"Loaded {df.shape[0]} rows")

    print("Reshaping data...")
    processed = reshape_symptom_df(df)
    print(f"After reshaping: {len(processed)} records")
    print(f"ICD-10 category distribution:\n{processed['icd_category'].value_counts()}\n")

    # add binary label vectors
    processed["labels"] = processed["icd_category"].apply(make_label_vector)

    # 70/15/15 split
    train_df, temp_df = train_test_split(processed, test_size=0.30, random_state=42, stratify=processed["icd_category"])
    val_df, test_df = train_test_split(temp_df, test_size=0.50, random_state=42)

    train_df.to_csv(f"{OUTPUT_DIR}/train.csv", index=False)
    val_df.to_csv(f"{OUTPUT_DIR}/val.csv", index=False)
    test_df.to_csv(f"{OUTPUT_DIR}/test.csv", index=False)

    # save the category list so classifier knows label order
    import json
    with open(f"{OUTPUT_DIR}/categories.json", "w") as f:
        json.dump(ALL_CATEGORIES, f, indent=2)

    print(f"Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")
    print(f"Saved splits to {OUTPUT_DIR}/")
    print(f"Categories ({len(ALL_CATEGORIES)}): {ALL_CATEGORIES}")


if __name__ == "__main__":
    main()
