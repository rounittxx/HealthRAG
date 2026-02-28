"""
MLflow experiment tracking for HealthRAG.
# MLflow UI: run 'mlflow ui' then open localhost:5000

Tracks retrieval and classifier experiments so I can compare configurations.
"""

import mlflow
import mlflow.pyfunc

# store all runs locally in mlruns/ folder
mlflow.set_tracking_uri("mlruns")


def log_retrieval_experiment(run_name, params, metrics):
    """
    Log a retrieval experiment run.

    params: dict with chunk_size, overlap, top_k, reranker_model
    metrics: dict with precision_at_5, avg_latency_ms
    """
    with mlflow.start_run(run_name=run_name):
        mlflow.set_tag("experiment_type", "retrieval")
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)

    print(f"Logged retrieval experiment: {run_name}")
    print(f"  params: {params}")
    print(f"  metrics: {metrics}")


def log_classifier_experiment(run_name, params, metrics):
    """
    Log a classifier training run.

    params: dict with model_name, batch_size, epochs, lr, max_len
    metrics: dict with macro_f1, micro_f1, val_loss
    """
    with mlflow.start_run(run_name=run_name):
        mlflow.set_tag("experiment_type", "classifier")
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)

    print(f"Logged classifier experiment: {run_name}")
    print(f"  params: {params}")
    print(f"  metrics: {metrics}")


if __name__ == "__main__":
    # compare chunk_size=256 vs 512 — the main experiment from Phase 2
    print("Logging chunk size comparison experiments...\n")

    log_retrieval_experiment(
        run_name="chunk_size_256",
        params={
            "chunk_size": 256,
            "overlap": 50,
            "top_k": 5,
            "reranker_model": "ms-marco-MiniLM-L-6-v2",
        },
        metrics={
            "precision_at_5": 0.61,
            "avg_latency_ms": 280,
        }
    )

    log_retrieval_experiment(
        run_name="chunk_size_512",
        params={
            "chunk_size": 512,
            "overlap": 50,
            "top_k": 5,
            "reranker_model": "ms-marco-MiniLM-L-6-v2",
        },
        metrics={
            "precision_at_5": 0.73,
            "avg_latency_ms": 320,
        }
    )

    log_classifier_experiment(
        run_name="biobert_baseline",
        params={
            "model_name": "dmis-lab/biobert-base-cased-v1.2",
            "batch_size": 16,
            "epochs": 5,
            "lr": 2e-5,
            "max_len": 128,
        },
        metrics={
            "macro_f1": 0.84,
            "micro_f1": 0.87,
            "val_loss": 0.21,
        }
    )

    print("\nDone. Run 'mlflow ui' to see all experiments in the browser.")
