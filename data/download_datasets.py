# Run this once to get all datasets
# Downloads MedQuAD from GitHub and expects the Kaggle CSV to already be placed at data/raw/

import os
import requests
import zipfile
import io

# where we want everything to land
RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

# MedQuAD is a public GitHub repo with 47K medical QA pairs from NIH
MEDQUAD_REPO_ZIP = "https://github.com/abachaa/MedQuAD/archive/refs/heads/master.zip"

def download_medquad():
    print("Downloading MedQuAD dataset from GitHub...")
    try:
        response = requests.get(MEDQUAD_REPO_ZIP, stream=True)
        response.raise_for_status()

        total = 0
        chunks = []
        for chunk in response.iter_content(chunk_size=8192):
            chunks.append(chunk)
            total += len(chunk)
            if total % (1024 * 1024) == 0:
                print(f"  Downloaded {total // (1024*1024)} MB so far...")

        print(f"  Done. Total size: {total / (1024*1024):.1f} MB")

        # unzip into data/raw/MedQuAD
        print("Extracting MedQuAD...")
        zip_data = io.BytesIO(b"".join(chunks))
        with zipfile.ZipFile(zip_data) as zf:
            zf.extractall(RAW_DIR)

        # the folder comes out as MedQuAD-master — rename for consistency
        extracted_path = os.path.join(RAW_DIR, "MedQuAD-master")
        final_path = os.path.join(RAW_DIR, "MedQuAD")
        if os.path.exists(extracted_path) and not os.path.exists(final_path):
            os.rename(extracted_path, final_path)

        print(f"MedQuAD saved to {final_path}")

    except Exception as e:
        print(f"Download failed: {e}")
        print("Try manually cloning: git clone https://github.com/abachaa/MedQuAD data/raw/MedQuAD")


def check_kaggle_csv():
    # I'm assuming you placed the Kaggle dataset manually here
    # Download from: https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset
    expected_path = os.path.join(RAW_DIR, "symptom_disease.csv")
    if os.path.exists(expected_path):
        print(f"Kaggle symptom CSV found at {expected_path}")
    else:
        print(f"[!] Kaggle CSV not found at {expected_path}")
        print("    Please download it from Kaggle and place it at data/raw/symptom_disease.csv")
        print("    Dataset: https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset")


if __name__ == "__main__":
    download_medquad()
    check_kaggle_csv()
    print("\nAll done! Run data_loader.py next to parse the datasets.")
