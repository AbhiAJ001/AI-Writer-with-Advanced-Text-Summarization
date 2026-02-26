import unittest
from app import app
from unittest.mock import patch, MagicMock
import json

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_health_check(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'healthy')

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AI Text Summarizer', response.data)

    @patch('app.summarize_text')
    @patch('app.extract_keywords')
    @patch('app.calculate_metrics')
    def test_summarize_text_api(self, mock_metrics, mock_keywords, mock_summarize):
        # Mock returns
        mock_summarize.return_value = "This is a summary."
        mock_keywords.return_value = ["test", "keyword"]
        mock_metrics.return_value = {"input_word_count": 10, "summary_word_count": 4, "compression_ratio": 60, "readability_score": 80}

        long_text = "This is a test input text for summarization. " * 5
        response = self.client.post('/summarize', data={'text': long_text})

        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data['summary'], "This is a summary.")
        self.assertEqual(len(data['keywords']), 2)
        self.assertIn('metrics', data)

    @patch('app.extract_text_from_pdf')
    @patch('app.summarize_text')
    @patch('app.extract_keywords')
    @patch('app.calculate_metrics')
    def test_summarize_pdf_api(self, mock_metrics, mock_keywords, mock_summarize, mock_pdf_extract):
        # Mock returns
        mock_pdf_extract.return_value = "Extracted PDF text. " * 5
        mock_summarize.return_value = "Summary of PDF."
        mock_keywords.return_value = ["pdf", "summary"]
        mock_metrics.return_value = {"input_word_count": 3, "summary_word_count": 3, "compression_ratio": 0, "readability_score": 50}

        # Create a dummy PDF file (StringIO won't work for file upload directly in Flask test client usually, need BytesIO)
        from io import BytesIO
        data = {
            'file': (BytesIO(b'Dummy PDF content'), 'test.pdf'),
            'model': 'standard',
            'length': 'medium'
        }

        response = self.client.post('/summarize', data=data, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['summary'], "Summary of PDF.")
        mock_pdf_extract.assert_called_once()

    def test_invalid_input(self):
        response = self.client.post('/summarize', data={'text': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn('No text provided', response.json['error'])

        response = self.client.post('/summarize', data={'text': 'short'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('too short', response.json['error'])

if __name__ == '__main__':
    unittest.main()
