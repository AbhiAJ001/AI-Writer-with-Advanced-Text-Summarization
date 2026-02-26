import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, BartTokenizer, BartForConditionalGeneration

# Constants
MAX_CHUNK_LENGTH_T5 = 512
MAX_CHUNK_LENGTH_BART = 1024

# Global variables for models
t5_model = None
t5_tokenizer = None
bart_model = None
bart_tokenizer = None

def load_models():
    """
    Loads models into memory.
    """
    global t5_model, t5_tokenizer, bart_model, bart_tokenizer

    if t5_model is None:
        print("Loading T5-small model...")
        t5_tokenizer = T5Tokenizer.from_pretrained("t5-small", model_max_length=512)
        t5_model = T5ForConditionalGeneration.from_pretrained("t5-small")

    if bart_model is None:
        print("Loading BART-base model...")
        # Using facebook/bart-base as requested. Note: efficient summarization usually requires fine-tuning (e.g. bart-large-cnn).
        bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-base", model_max_length=1024)
        bart_model = BartForConditionalGeneration.from_pretrained("facebook/bart-base")

    print("Models loaded.")

def chunk_text(text, tokenizer, max_length):
    """
    Splits text into chunks.
    """
    inputs = tokenizer(text, return_tensors="pt", add_special_tokens=False)
    input_ids = inputs["input_ids"][0]

    chunks = []
    chunk_size = max_length - 20 # Safety margin

    # If text is shorter than chunk size, just return it
    if len(input_ids) <= chunk_size:
        return [text]

    for i in range(0, len(input_ids), chunk_size):
        chunk_ids = input_ids[i : i + chunk_size]
        chunks.append(tokenizer.decode(chunk_ids, skip_special_tokens=True))

    return chunks

def get_generation_params(length_setting):
    """
    Returns generation parameters based on length setting.
    """
    if length_setting == "short":
        return {"max_length": 150, "min_length": 30, "length_penalty": 2.0, "num_beams": 4}
    elif length_setting == "medium":
        return {"max_length": 300, "min_length": 80, "length_penalty": 2.0, "num_beams": 4}
    elif length_setting == "detailed":
        return {"max_length": 500, "min_length": 150, "length_penalty": 1.0, "num_beams": 4}
    else:
        return {"max_length": 300, "min_length": 80, "length_penalty": 2.0, "num_beams": 4}

def summarize_chunk(text, model, tokenizer, params, is_t5=True):
    """
    Summarizes a single chunk of text.
    """
    prefix = "summarize: " if is_t5 else ""
    input_text = prefix + text

    inputs = tokenizer(input_text, return_tensors="pt", max_length=512 if is_t5 else 1024, truncation=True)

    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=params["max_length"],
        min_length=params["min_length"],
        length_penalty=params["length_penalty"],
        num_beams=params["num_beams"],
        early_stopping=True
    )

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def summarize_text(text, model_type="standard", length_setting="medium"):
    """
    Main function to summarize text.
    """
    global t5_model, t5_tokenizer, bart_model, bart_tokenizer

    if t5_model is None or bart_model is None:
        load_models()

    if model_type == "pro":
        model = bart_model
        tokenizer = bart_tokenizer
        max_len = MAX_CHUNK_LENGTH_BART
        is_t5 = False
    else:
        model = t5_model
        tokenizer = t5_tokenizer
        max_len = MAX_CHUNK_LENGTH_T5
        is_t5 = True

    chunks = chunk_text(text, tokenizer, max_len)
    params = get_generation_params(length_setting)

    summaries = []
    for chunk in chunks:
        summary = summarize_chunk(chunk, model, tokenizer, params, is_t5)
        summaries.append(summary)

    final_summary = " ".join(summaries)
    return final_summary
