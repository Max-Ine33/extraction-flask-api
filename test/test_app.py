import unittest
import os
import sys

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from src.app import app, db
from src.models import Article, Author


class AppTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test client and configure the app for testing
        app.config["TESTING"] = True
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
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<h1>Welcome to this API", response.data)
        self.assertIn(b'<a href="/articles">View Articles</a>', response.data)
        self.assertIn(b'<a href="/about">About this API</a>', response.data)

    def test_about_page(self):
        response = self.app.get("/about")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<h1>About</h1>", response.data)

    def test_articles(self):
        response = self.app.get("/articles")
        self.assertEqual(response.status_code, 200)

    def test_upload_new_article(self):
        data = {
            "id": "test_article",
            "title": "Test Article",
            "summary": "This is a test article.",
            "published_date": "2024-01-27",
            "updated_date": "2024-01-27",
            "doi": "doi:1234/test",
            "comment": "Test comment",
            "journal_reference": "Test Journal",
        }

        with app.app_context():
            new_article = Article(
                id=data["id"],
                title=data["title"],
                summary=data["summary"],
                published_date=data["published_date"],
                updated_date=data["updated_date"],
                doi=data["doi"],
                comment=data["comment"],
                journal_reference=data["journal_reference"],
            )
            db.session.add(new_article)
            db.session.commit()

            retrieved_article = db.session.get(Article, data["id"])
            self.assertIsNotNone(retrieved_article)

        response = self.app.get(f'/articles/{data["id"]}')
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertIn("article", result)

    def test_auto_populate(self):
        response = self.app.get("/auto_populate")
        self.assertEqual(response.status_code, 200)
        # Add assertions based on the expected behavior of the auto_populate route

    def test_empty_database_post_confirmation_yes(self):
        response = self.app.post("/empty_database", data={"confirmation": "yes"})
        self.assertEqual(response.status_code, 200)
        # Add assertions based on the expected behavior after confirming deletion

    def test_empty_database_post_confirmation_no(self):
        response = self.app.post("/empty_database", data={"confirmation": "no"})
        self.assertEqual(response.status_code, 200)
        # Add assertions based on the expected behavior after canceling deletion


if __name__ == "__main__":
    unittest.main()
