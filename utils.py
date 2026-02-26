import pdfplumber
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import textstat

def extract_text_from_pdf(filepath):
    """
    Extracts text from a PDF file using pdfplumber.
    """
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

    return clean_text(text)

def clean_text(text):
    """
    Basic text cleaning: removes excessive whitespace.
    """
    if not text:
        return ""
    # Replace multiple newlines/tabs/spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_keywords(text, top_n=10):
    """
    Extracts top N keywords using TF-IDF.
    """
    if not text:
        return []

    # We need a collection of documents for TF-IDF to work properly,
    # but here we have only one document. We can simulate a corpus
    # or just use stop words removal and frequency.
    # For a single document, TF-IDF is essentially term frequency (TF)
    # with stop word removal.

    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=top_n)
        tfidf_matrix = vectorizer.fit_transform([text])
        feature_names = vectorizer.get_feature_names_out()

        # Get scores
        dense = tfidf_matrix.todense()
        episode = dense[0].tolist()[0]
        phrase_scores = [pair for pair in zip(range(0, len(episode)), episode) if pair[1] > 0]

        sorted_phrase_scores = sorted(phrase_scores, key=lambda t: t[1] * -1)
        keywords = [feature_names[i] for i, _ in sorted_phrase_scores]

        return keywords
    except ValueError:
        # This can happen if the text is empty or only contains stop words
        return []

def calculate_metrics(original_text, summary_text):
    """
    Calculates metrics: Input word count, Summary word count,
    Compression ratio, Flesch Reading Ease.
    """
    input_word_count = len(original_text.split())
    summary_word_count = len(summary_text.split())

    compression_ratio = 0
    if input_word_count > 0:
        compression_ratio = (1 - (summary_word_count / input_word_count)) * 100

    readability_score = textstat.flesch_reading_ease(summary_text)

    return {
        "input_word_count": input_word_count,
        "summary_word_count": summary_word_count,
        "compression_ratio": round(compression_ratio, 2),
        "readability_score": readability_score
    }
