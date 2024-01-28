import unittest
import os
import sys
import json
import sys

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from unittest.mock import patch, Mock
from pathlib import Path
from src.app import app, db
from src.utils import (
    article_to_dict,
    get_arxiv_articles,
    fetch_summary_by_id,
    populate_single_article,
    populate_articles_by_query,
)
from src.models import Article, Author


class UtilsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Mock the response from requests.get globally
        cls.patcher = patch("src.utils.requests.get")
        cls.mock_requests_get = cls.patcher.start()

    @classmethod
    def tearDownClass(cls):
        # Stop patching requests.get
        cls.patcher.stop()

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
        # Test for get_arxiv_articles
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

    def test_fetch_summary_by_id(self):
        # Test for fetch_summary_by_id
        article_id = "2401.13999"
        mock_response = Mock()

        # Read the mocked response from the file
        file_path = (
            Path(__file__).parent / "test_data" / "2401.13999-arxiv.xml"
        ).resolve()
        with open(file_path, "r") as file:
            mock_response.text = file.read()

        self.mock_requests_get.return_value = mock_response

        # Call the function that fetches the summary
        result = fetch_summary_by_id(article_id)

        # Read the expected output from the file
        expected_summary_path = (
            Path(__file__).parent / "test_data" / "2401.13999-summary.txt"
        ).resolve()
        with open(expected_summary_path, "r") as expected_file:
            expected_summary = expected_file.read()

        # Modify the assertion to check for a substring
        self.assertEqual(expected_summary, result)


    def test_populate_single_article(self):
        # Test for populate_single_article
        article_id = "new_test_article"

        # Read the content of the template response from the file
        template_response_path = (
            Path(__file__).parent / "test_data" / "2401.13999-arxiv.xml"
        ).resolve()

        with open(template_response_path, "r") as template_file:
            template_response_content = template_file.read()

        # Create a mock response with the template content
        mock_response = Mock()
        mock_response.text = template_response_content

        # Set up the mock to return the mocked response when the arXiv API is called
        with app.app_context(), patch("src.utils.requests.get", return_value=mock_response):
            # Call the function that populates a single article
            article_id = "2401.13999"
            result = populate_single_article(article_id)

            # Extract the Flask response object and status code
            flask_response = result
            status_code = flask_response.status_code

            # Check if the status code indicates success (e.g., 200 OK)
            self.assertEqual(status_code, 200)

            # Extract the message from the JSON response
            response_message = flask_response.get_json().get("message", "")

            # Check if the message indicates success
            self.assertIn("Article added to the database successfully", response_message)

            # Check if the article is now in the database
            response = self.app.get(f'/articles/{article_id}')
            self.assertEqual(response.status_code, 200)  # Article in the database

            # Try to populate the same article again
            result_duplicate = populate_single_article(article_id)

            # Check if the response indicates that the article already exists
            self.assertEqual(result_duplicate[1], 400)


    def test_populate_articles_by_query(self):
        # Test for populate_articles_by_query
        query = "test"
        max_results = 5

        with app.test_request_context():
            # Call the function that populates articles by query
            response = populate_articles_by_query(query, max_results)

            # Check if the response indicates success
            result = response.get_json()
            self.assertIn("message", result)




if __name__ == "__main__":
    unittest.main()
