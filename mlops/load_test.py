"""
Locust load test for the HealthRAG API.
Simulates 50 concurrent users sending medical questions.

Run with: locust -f mlops/load_test.py --host http://localhost:8000
Then open http://localhost:8089 for the web UI.
"""

from locust import HttpUser, task, between
import random

SAMPLE_QUERIES = [
    "what are the symptoms of diabetes?",
    "how is hypertension treated?",
    "what causes asthma?",
    "what is multiple sclerosis?",
    "how do I manage high cholesterol?",
    "what are the signs of a heart attack?",
    "what is the treatment for pneumonia?",
    "what are the symptoms of kidney disease?",
    "what is rheumatoid arthritis?",
    "how is depression diagnosed?",
    "what causes migraines?",
    "what is type 1 vs type 2 diabetes?",
    "what are the side effects of ibuprofen?",
    "how does the immune system fight infection?",
    "what is osteoporosis?",
]

SYMPTOM_QUERIES = [
    "fever and chills",
    "persistent cough and shortness of breath",
    "chest pain and dizziness",
    "severe headache and light sensitivity",
    "joint pain and swelling",
]


class HealthRAGUser(HttpUser):
    # each simulated user waits 1–3 seconds between requests (realistic pace)
    wait_time = between(1, 3)

    @task(3)  # 3x more likely to hit /ask than /classify
    def ask_question(self):
        query = random.choice(SAMPLE_QUERIES)
        self.client.post("/ask", json={"query": query, "history": []})

    @task(1)
    def classify_symptoms(self):
        symptoms = random.choice(SYMPTOM_QUERIES)
        self.client.post("/classify", json={"symptoms": symptoms})

    @task(1)
    def health_check(self):
        self.client.get("/health")
