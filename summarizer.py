import os
import requests

# Hugging Face Inference API
HF_API_URL = "https://router.huggingface.co/hf-inference/models/"
HF_API_TOKEN = os.environ.get("HF_API_TOKEN", "")

# Model endpoints
STANDARD_MODEL = "sshleifer/distilbart-cnn-12-6"
PRO_MODEL = "facebook/bart-large-cnn"

def get_headers():
    """Returns headers for HF API requests."""
    headers = {}
    if HF_API_TOKEN:
        headers["Authorization"] = f"Bearer {HF_API_TOKEN}"
    return headers

def load_models():
    """
    No-op when using HF Inference API. Models are hosted remotely.
    """
    print("Using Hugging Face Inference API - no local model loading needed.")

def get_generation_params(length_setting):
    """
    Returns generation parameters based on length setting.
    """
    if length_setting == "short":
        return {"max_length": 150, "min_length": 30}
    elif length_setting == "medium":
        return {"max_length": 300, "min_length": 80}
    elif length_setting == "detailed":
        return {"max_length": 500, "min_length": 150}
    else:
        return {"max_length": 300, "min_length": 80}

def chunk_text(text, max_chunk_chars=3000):
    """
    Splits text into chunks by character count for API calls.
    """
    if len(text) <= max_chunk_chars:
        return [text]

    chunks = []
    words = text.split()
    current_chunk = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_chunk_chars and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def summarize_chunk_api(text, model_id, params):
    """
    Summarizes a single chunk using the HF Inference API.
    """
    url = HF_API_URL + model_id
    input_text = text

    payload = {
        "inputs": input_text,
        "parameters": {
            "max_length": params["max_length"],
            "min_length": params["min_length"],
        },
        "options": {
            "wait_for_model": True
        }
    }

    response = requests.post(url, headers=get_headers(), json=payload, timeout=120)

    if response.status_code != 200:
        raise Exception(f"HF API error ({response.status_code}): {response.text}")

    result = response.json()

    if isinstance(result, list) and len(result) > 0:
        return result[0].get("summary_text", result[0].get("generated_text", ""))
    elif isinstance(result, dict):
        return result.get("summary_text", result.get("generated_text", ""))
    else:
        raise Exception(f"Unexpected API response format: {result}")

def summarize_text(text, model_type="standard", length_setting="medium"):
    """
    Main function to summarize text using HF Inference API.
    """
    if model_type == "pro":
        model_id = PRO_MODEL
        max_chunk_chars = 4000
    else:
        model_id = STANDARD_MODEL
        max_chunk_chars = 3000

    chunks = chunk_text(text, max_chunk_chars)
    params = get_generation_params(length_setting)

    summaries = []
    for chunk in chunks:
        summary = summarize_chunk_api(chunk, model_id, params)
        summaries.append(summary)

    final_summary = " ".join(summaries)
    return final_summary
