"""
Evidently AI data drift monitoring for HealthRAG.
Checks if incoming user queries have drifted from the training data distribution.
Run periodically (e.g. weekly) to catch distribution shift early.
"""

import os
import json
import pandas as pd
import numpy as np

try:
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset, TextOverviewPreset
    HAS_EVIDENTLY = True
except ImportError:
    print("[!] Install evidently: pip install evidently")
    HAS_EVIDENTLY = False

os.makedirs("mlops/drift_reports", exist_ok=True)


def load_reference_queries(path="data/processed/chunks_meta.json", n=500):
    """
    Use a sample of training chunk texts as the reference distribution.
    """
    with open(path) as f:
        meta = json.load(f)

    texts = [m["text"][:300] for m in meta[:n]]  # first 300 chars is enough
    return pd.DataFrame({"query": texts})


def load_production_queries(path="mlops/production_queries.json"):
    """
    Load actual user queries logged from the API.
    In production these would come from a database or log file.
    """
    if not os.path.exists(path):
        # generate some fake queries for demo purposes
        print("[!] No production queries found, generating synthetic ones")
        fake = [
            "what are the symptoms of diabetes",
            "how to treat high blood pressure",
            "what causes asthma attacks",
            "is ibuprofen safe for children",
            "what are the side effects of metformin",
        ] * 20
        return pd.DataFrame({"query": fake})

    with open(path) as f:
        data = json.load(f)

    return pd.DataFrame({"query": data})


def run_drift_check():
    """
    Generate an Evidently drift report comparing reference vs production queries.
    Saves the report as HTML.
    """
    if not HAS_EVIDENTLY:
        print("[!] Evidently not installed. Skipping drift check.")
        return

    if not os.path.exists("data/processed/chunks_meta.json"):
        print("[!] chunks_meta.json not found. Run embed_chunks.py first.")
        return

    print("Loading reference and production data...")
    reference = load_reference_queries()
    production = load_production_queries()

    print(f"Reference: {len(reference)} samples")
    print(f"Production: {len(production)} samples")

    # run Evidently drift report
    report = Report(metrics=[
        DataDriftPreset(),
    ])

    report.run(reference_data=reference, current_data=production)

    report_path = "mlops/drift_reports/drift_report.html"
    report.save_html(report_path)
    print(f"Drift report saved to {report_path}")
    print("Open it in a browser to see if any features have drifted.")


def log_production_query(query, output_path="mlops/production_queries.json"):
    """
    Log a production query for drift monitoring.
    Call this from the API after each /ask request.
    """
    queries = []
    if os.path.exists(output_path):
        with open(output_path) as f:
            try:
                queries = json.load(f)
            except json.JSONDecodeError:
                queries = []

    queries.append(query)

    # keep last 5000 queries
    if len(queries) > 5000:
        queries = queries[-5000:]

    with open(output_path, "w") as f:
        json.dump(queries, f)


if __name__ == "__main__":
    run_drift_check()
