import unittest
from unittest.mock import patch
from flask import json
from final_merged import app

class FinalMergedTestCase(unittest.TestCase):
    
    def setUp(self):
        # Creating a test client
        self.app = app.test_client()
        
    @patch('final_merged.translate_text')
    @patch('final_merged.summarize_text')
    @patch('final_merged.Article')
    @patch('final_merged.feedparser.parse')
    def test_get_articles(self, mock_parse, mock_Article, mock_summarize_text, mock_translate_text):
        # Test values for the 'country', 'topic', and 'language' parameters
        test_country = 'USA'
        test_topic = 'technology'
        test_language = 'en'
        
        # Expected response
        expected_response = [
            {
                'title': 'Test Article 1',
                'summary': 'This is the first test article.'
            },
            {
                'title': 'Test Article 2',
                'summary': 'This is the second test article.'
            }
        ]
        
        # Mocking the feedparser library to return the test RSS feed
        test_rss_feed = {
            'entries': [
                {'title': 'Test Article 1', 'link': 'https://example.com/test_article_1'},
                {'title': 'Test Article 2', 'link': 'https://example.com/test_article_2'}
            ]
        }
        mock_parse.return_value = test_rss_feed
        
        # Mocking the Article class from the newspaper library
        mock_article = Mock()
        mock_article.title = 'Test Article'
        mock_article.text = 'This is a test article.'
        mock_Article.return_value = mock_article
        
        # Mocking the summarize_text function
        mock_summarize_text.return_value = 'This is a test article.'
        
        # Mocking the translate_text function
        mock_translate_text.return_value = 'This is a test article.'
        
        # Sending a GET request to the get_articles endpoint
        response = self.app.get(f'/get_articles?country={test_country}&topic={test_topic}&language={test_language}')
        
        # Validating the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), expected_response)

# Running the tests
if __name__ == '__main__':
    unittest.main()