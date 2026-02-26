from flask import Flask, request, jsonify, render_template
from flask_caching import Cache
import os
from werkzeug.utils import secure_filename
from utils import extract_text_from_pdf, extract_keywords, calculate_metrics, clean_text
from summarizer import summarize_text, load_models

app = Flask(__name__)

# Ensure uploads directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Configure caching
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})

# Load models on startup (optional but recommended for reliability)
# Ideally, we call load_models() here, but it might slow down initial startup.
# Given the PRD "Model loaded once at startup", we should call it.
# However, for development speed, let's call it on first request or explicitly.
# We'll call it here inside a try-except to not break if import fails.
if os.environ.get('SKIP_MODEL_LOAD') != 'true':
    try:
        load_models()
    except Exception as e:
        print(f"Error loading models on startup: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "AI Writer API"})

@app.route('/summarize', methods=['POST'])
def summarize():
    text = ""

    # Handle File Upload
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and file.filename.endswith('.pdf'):
            # Save temporary file
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads', filename)
            file.save(filepath)

            # Extract text
            extracted_text = extract_text_from_pdf(filepath)

            # Clean up
            os.remove(filepath)

            if not extracted_text:
                return jsonify({"error": "Could not extract text from PDF"}), 400

            text = extracted_text
        else:
            return jsonify({"error": "Invalid file type. Only PDF allowed."}), 400

    # Handle Text Input
    elif 'text' in request.form:
        text = request.form['text']
    else:
        # Check if json body
        data = request.get_json(silent=True)
        if data and 'text' in data:
            text = data['text']

    if not text:
        return jsonify({"error": "No text provided"}), 400

    text = clean_text(text)
    if len(text) < 50:
        return jsonify({"error": "Text too short to summarize"}), 400

    # Get parameters
    model_type = request.form.get('model', 'standard')
    length_setting = request.form.get('length', 'medium')

    # JSON body override
    if request.is_json:
        data = request.get_json()
        model_type = data.get('model', model_type)
        length_setting = data.get('length', length_setting)

    # Check cache
    import hashlib
    content_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
    cache_key = f"{content_hash}-{model_type}-{length_setting}"
    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)

    try:
        # Summarize
        summary = summarize_text(text, model_type=model_type, length_setting=length_setting)

        # Keywords
        keywords = extract_keywords(text)

        # Metrics
        metrics = calculate_metrics(text, summary)

        response = {
            "summary": summary,
            "keywords": keywords,
            "metrics": metrics
        }

        # Set cache
        cache.set(cache_key, response)

        return jsonify(response)

    except Exception as e:
        print(f"Error during summarization: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
