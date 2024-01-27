import unittest
import os
import sys
# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.app import app, db
from src.models import Article, Author
from src.utils import get_arxiv_articles, fetch_summary_by_id, populate_single_article, populate_articles_by_query

class AppTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test client and configure the app for testing
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            # Create a test database
            db.create_all()

    def tearDown(self):
        # Clean up the test database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # ACTUAL TESTS

    # Tests for each page
    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Homepage')

    def test_articles(self):
        response = self.app.get('/articles')
        self.assertEqual(response.status_code, 200)


    def test_upload_new_article(self):
        # Test uploading a new article
        data = {
            "id": "test_article",
            "title": "Test Article",
            "summary": "This is a test article.",
            "published_date": "2024-01-27",
            "updated_date": "2024-01-27",
            "doi": "doi:1234/test",
            "comment": "Test comment",
            "journal_reference": "Test Journal"
        }

        with app.app_context():
            # Create and commit the new article
            new_article = Article(
                id=data["id"],
                title=data["title"],
                summary=data["summary"],
                published_date=data["published_date"],
                updated_date=data["updated_date"],
                doi=data["doi"],
                comment=data["comment"],
                journal_reference=data["journal_reference"]
            )
            db.session.add(new_article)
            db.session.commit()

            # Fetch the uploaded article using Session.get()
            retrieved_article = db.session.get(Article, data["id"])
            self.assertIsNotNone(retrieved_article)

        # Make a GET request to fetch the uploaded article
        response = self.app.get(f'/articles/{data["id"]}')
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertIn("article", result)


if __name__ == '__main__':
    unittest.main()
