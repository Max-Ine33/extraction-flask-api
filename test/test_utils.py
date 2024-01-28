import unittest
import os
import sys

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from src.app import app, db
from unittest.mock import patch, Mock
from src.utils import (
    article_to_dict,
    get_arxiv_articles,
    fetch_summary_by_id,
    populate_single_article,
    populate_articles_by_query,
)
from src.models import Article, Author
from pathlib import Path
import json


class UtilsTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test client and configure the app for testing
        app.config["TESTING"] = True
        self.app = app.test_client()

        with app.app_context():
            # Create a test database and insert some test data
            db.create_all()

            # Insert test data into the Article table
            test_article_1 = Article(
                id="test_article_1",
                title="Test Article 1",
                summary="Summary 1",
                published_date="2024-01-27",
            )
            test_article_2 = Article(
                id="test_article_2",
                title="Test Article 2",
                summary="Summary 2",
                published_date="2024-01-28",
            )

            db.session.add(test_article_1)
            db.session.add(test_article_2)
            db.session.commit()

    def tearDown(self):
        # Clean up the test database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_article_to_dict(self):
        # Test converting Article object to dictionary
        article_object = Article(
            id="test_article",
            title="Test Article",
            summary="This is a test article.",
            published_date="2024-01-27",
            updated_date="2024-01-28",
            doi="doi:1234/test",
            comment="Test comment",
            journal_reference="Test Journal",
            # You may need to add other fields as needed
        )

        # Add authors to the article
        author1 = Author(name="Author 1", article=article_object)
        author2 = Author(name="Author 2", article=article_object)
        article_object.authors = [author1, author2]

        # Convert the Article object to a dictionary
        result_dict = article_to_dict(article_object)

        # Define the expected dictionary
        expected_dict = {
            "id": "test_article",
            "title": "Test Article",
            "summary": "This is a test article.",
            "published_date": "2024-01-27",
            "updated_date": "2024-01-28",
            "doi": "doi:1234/test",
            "comment": "Test comment",
            "journal_reference": "Test Journal",
            "authors": [{"name": "Author 1"}, {"name": "Author 2"}],
        }

        self.assertIsInstance(result_dict, dict)
        self.assertEqual(result_dict, expected_dict)

    @patch("src.utils.requests.get")
    def test_get_arxiv_articles(self, mock_requests_get):
        # Mock the response from requests.get
        mock_response = Mock()

        # Read the mocked response from the file
        file_path = (
            Path(__file__).parent / "test_data" / "2401.13999-arxiv.xml"
        ).resolve()
        with open(file_path, "r") as file:
            mock_response.text = file.read()

        mock_requests_get.return_value = mock_response

        # Call the function that makes the HTTP request
        result = get_arxiv_articles(query="all", start=0, max_results=1)

        # Read the expected output from the file
        expected_output_path = (
            Path(__file__).parent / "test_data" / "2401.13999-function.json"
        ).resolve()
        with open(expected_output_path, "r") as expected_file:
            expected_output = json.load(expected_file)

        # Ignore differences in representation
        self.assertEqual(
            json.dumps(result[0], sort_keys=True),
            json.dumps(expected_output, sort_keys=True),
        )


if __name__ == "__main__":
    unittest.main()
