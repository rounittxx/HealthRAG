"""
Maps ICD-10 categories to specialist types.
Simple rule-based routing — works well for most common cases.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classifier.inference import classify_symptoms

# map each ICD-10 category to a specialist + reasoning
ICD_TO_SPECIALIST = {
    "Endocrine":        ("Endocrinologist",     "Endocrine conditions like diabetes or thyroid disorders are managed by endocrinologists."),
    "Respiratory":      ("Pulmonologist",        "Respiratory symptoms like persistent cough or breathing difficulty are evaluated by pulmonologists."),
    "Cardiovascular":   ("Cardiologist",         "Heart and blood pressure conditions require a cardiologist's assessment."),
    "Neurological":     ("Neurologist",          "Neurological symptoms affecting the brain, spine, or nerves need a neurologist."),
    "Gastrointestinal": ("Gastroenterologist",   "Digestive system conditions including liver and stomach issues are managed by gastroenterologists."),
    "Musculoskeletal":  ("Rheumatologist",       "Joint pain, arthritis, and musculoskeletal conditions are assessed by rheumatologists."),
    "Dermatological":   ("Dermatologist",        "Skin conditions and rashes are diagnosed and treated by dermatologists."),
    "Infectious":       ("Infectious Disease Specialist", "Infections like malaria, dengue or HIV require specialist infectious disease care."),
    "Mental Health":    ("Psychiatrist",         "Mental health conditions like depression and anxiety are treated by psychiatrists."),
    "Hematological":    ("Hematologist",         "Blood disorders like anaemia or clotting issues are managed by haematologists."),
    "Renal":            ("Nephrologist",         "Kidney conditions including CKD and kidney stones are handled by nephrologists."),
    "Other":            ("General Physician",    "A general physician can evaluate and route you to the right specialist."),
    "Unknown":          ("General Physician",    "Symptoms were not clearly classified. Start with a general physician for initial assessment."),
}


def recommend_specialist(icd_categories):
    """
    Given a list of (icd_category, confidence) tuples from the classifier,
    return the most appropriate specialist and a reason.

    If the top confidence is < 0.4, adds a note about seeing a GP first.
    """
    if not icd_categories:
        return "General Physician", "No clear classification — a GP is the best starting point."

    top_category, top_confidence = icd_categories[0]

    specialist, reason = ICD_TO_SPECIALIST.get(
        top_category,
        ("General Physician", "Condition category not recognised. Please see a GP first.")
    )

    # if confidence is low, add a recommendation to see GP first
    if top_confidence < 0.4:
        reason = f"Consider a General Physician first — confidence is low ({top_confidence:.2f}). {reason}"

    return specialist, reason


if __name__ == "__main__":
    test_query = "I have a persistent cough and shortness of breath"
    print(f"Test query: '{test_query}'\n")

    # classify first
    icd_results = classify_symptoms(test_query)
    print("ICD-10 classifications:")
    for cat, conf in icd_results:
        print(f"  {cat}: {conf:.3f}")

    # then recommend
    specialist, reason = recommend_specialist(icd_results)
    print(f"\nRecommended specialist: {specialist}")
    print(f"Reason: {reason}")
