"""
Thin wrapper around OpenAI API and Ollama (local LLM).
# start with OpenAI (costs a few cents), switch to Ollama once everything works
"""

import os
import requests
from openai import OpenAI
from config import USE_LOCAL_LLM, OPENAI_MODEL, LOCAL_MODEL

# load API key from env (you'll need your OpenAI key in a .env file)
_openai_client = None


def get_openai_client():
    global _openai_client
    if _openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set. Add it to your .env file.")
        _openai_client = OpenAI(api_key=api_key)
    return _openai_client


def call_openai(prompt, model=OPENAI_MODEL):
    """Call OpenAI chat completion API with a single user message."""
    client = get_openai_client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,  # low temp = more consistent, less creative (good for medical)
        max_tokens=600,
    )
    return response.choices[0].message.content.strip()


def call_ollama(prompt, model=LOCAL_MODEL):
    """
    Call local Ollama API.
    Make sure Ollama is running: ollama serve
    And model is pulled: ollama pull mistral
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3}
    }

    try:
        resp = requests.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        print("[!] Ollama not running. Start it with: ollama serve")
        raise
    except Exception as e:
        print(f"Ollama call failed: {e}")
        raise


def call_llm(prompt):
    """Route to the right LLM based on USE_LOCAL_LLM flag in config."""
    if USE_LOCAL_LLM:
        return call_ollama(prompt)
    else:
        return call_openai(prompt)

# temperature 0.3 keeps answers factual — higher values increase hallucination risk
