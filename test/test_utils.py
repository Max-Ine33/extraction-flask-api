import unittest
import os
import sys
# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from unittest.mock import patch, Mock
from src.utils import article_to_dict, get_arxiv_articles, fetch_summary_by_id, populate_single_article, populate_articles_by_query
from src.models import Article

class UtilsTestCase(unittest.TestCase):

    def test_article_to_dict(self):
        # Test converting Article object to dictionary
        article_object = Article(
            id="test_article",
            title="Test Article",
            summary="This is a test article.",
            published_date="2024-01-27"
        )
        result_dict = article_to_dict(article_object)

        self.assertIsInstance(result_dict, dict)
        self.assertEqual(result_dict['id'], "test_article")
        self.assertEqual(result_dict['title'], "Test Article")

    @patch('src.utils.requests.get')
    def test_get_arxiv_articles(self, mock_requests_get):
        # Mock the response from requests.get
        mock_response = Mock()
        mock_response.text = 'mocked response'
        mock_requests_get.return_value = mock_response

        # Call the function that makes the HTTP request
        result = get_arxiv_articles(query='test', start=0, max_results=5)

        # Assert that the function behaves as expected based on the mocked response
        self.assertEqual(len(result), 5)

if __name__ == '__main__':
    unittest.main()
