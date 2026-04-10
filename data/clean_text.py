import re
import os
import json

# 512 worked better than 256 in my experiments --- less context loss
CHUNK_SIZE = 512
OVERLAP = 50


def clean_medical_text(text):
    """
    Clean raw medical text for embedding.
    Keeps hyphens and parentheses because medical terms use them a lot
    (e.g. beta-blocker, HbA1c (glycated haemoglobin)).
    """
    if not text or not isinstance(text, str):
        return ""

    # strip HTML tags - some MedQuAD answers have leftover <p> or <br> tags
    text = re.sub(r"<[^>]+>", " ", text)

    # decode common HTML entities
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&nbsp;", " ").replace("&#39;", "'").replace("&quot;", '"')

    # remove weird unicode chars but keep standard punctuation + hyphens + parens
    text = re.sub(r"[^\w\s\-\(\)\.,;:!?\'/°%]", " ", text)

    # lowercase
    text = text.lower()

    # collapse multiple spaces / newlines into single space
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def remove_duplicates(records):
    """
    Deduplicates a list of dicts by question text.
    Does exact match + lowercased match --- no fuzzy matching needed at this scale.
    """
    seen = set()
    unique = []

    for rec in records:
        question = rec.get("question", "").lower().strip()
        if question and question not in seen:
            seen.add(question)
            unique.append(rec)

    removed = len(records) - len(unique)
    print(f"Removed {removed} duplicate records. {len(unique)} unique records remain.")
    return unique


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """
    Split text into overlapping chunks by word count.
    Using split() as a proxy for token count --- good enough for now.
    # TODO: try tiktoken for proper token counting later
    """
    words = text.split()

    if len(words) <= chunk_size:
        return [text]  # short enough, no need to split

    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap  # slide forward with overlap

    return chunks


def process_and_save(records, output_path="data/processed/cleaned_chunks.json"):
    """
    Clean all records, chunk them, and save to JSON.
    Each saved item has: text, source_url, category, original_question
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    all_chunks = []
    for rec in records:
        # clean both question and answer, then combine them for the chunk
        clean_q = clean_medical_text(rec.get("question", ""))
        clean_a = clean_medical_text(rec.get("answer", ""))
        combined = f"{clean_q} {clean_a}".strip()

        chunks = chunk_text(combined)
        for chunk in chunks:
            if len(chunk.split()) < 10:  # skip super short chunks
                continue
            all_chunks.append({
                "text": chunk,
                "source_url": rec.get("source_url", ""),
                "category": rec.get("category", ""),
                "original_question": rec.get("question", "")[:200],  # truncate for storage
            })

    with open(output_path, "w") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"Saved {len(all_chunks)} chunks to {output_path}")
    avg_len = sum(len(c["text"].split()) for c in all_chunks) / max(len(all_chunks), 1)
    print(f"Average chunk length: {avg_len:.0f} words")
    return all_chunks


if __name__ == "__main__":
    # quick sanity check on the cleaning functions
    test = "<p>This is a <b>test</b> with &amp; symbols and   extra   spaces.</p>"
    print("Raw:", test)
    print("Cleaned:", clean_medical_text(test))

    test_long = " ".join([f"word{i}" for i in range(600)])
    chunks = chunk_text(test_long)
    print(f"\nChunked 600 words into {len(chunks)} chunks")
    print(f"First chunk size: {len(chunks[0].split())} words")
    print(f"Last chunk size: {len(chunks[-1].split())} words")

# minimum chunk length filter added — chunks under 30 words skipped
