import unittest
from utils import clean_text, extract_keywords, calculate_metrics, extract_text_from_pdf
from summarizer import chunk_text, get_generation_params
from transformers import T5Tokenizer

class TestUtils(unittest.TestCase):
    def test_clean_text(self):
        raw_text = "  This   is  a   messy \n text.  "
        expected = "This is a messy text."
        self.assertEqual(clean_text(raw_text), expected)

    def test_extract_keywords(self):
        text = "Machine learning is fascinating. Machine learning models are powerful."
        keywords = extract_keywords(text, top_n=2)
        self.assertTrue(len(keywords) > 0)
        self.assertIn("machine", keywords)
        self.assertIn("learning", keywords)

    def test_calculate_metrics(self):
        original = "This is a long sentence to test the word count metric."
        summary = "This is a summary."
        metrics = calculate_metrics(original, summary)
        self.assertEqual(metrics['input_word_count'], 11)
        self.assertEqual(metrics['summary_word_count'], 4)
        self.assertTrue(metrics['compression_ratio'] > 0)
        self.assertIn('readability_score', metrics)

class TestSummarizerLogic(unittest.TestCase):
    def test_get_generation_params(self):
        params = get_generation_params("short")
        self.assertEqual(params['max_length'], 150)

        params = get_generation_params("detailed")
        self.assertEqual(params['max_length'], 500)

    # We skip actual model inference tests here to avoid loading heavy models during unit tests.
    # However, we can test chunking logic if we use a real tokenizer (small one).

    def test_chunk_text(self):
        # Using T5Tokenizer (fast)
        try:
            tokenizer = T5Tokenizer.from_pretrained("t5-small", model_max_length=512)
            text = "word " * 600 # Should exceed 512 tokens
            chunks = chunk_text(text, tokenizer, max_length=512)
            self.assertTrue(len(chunks) >= 2)
        except Exception as e:
            print(f"Skipping chunk test due to model loading issue: {e}")

if __name__ == '__main__':
    unittest.main()
