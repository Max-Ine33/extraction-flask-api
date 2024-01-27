import unittest
import os
import sys
# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.app import app, db
from src.models import Article, Author

class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test database
        app.config['TESTING'] = True
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the test database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_article_model(self):
        # Test creating and querying an Article
        with app.app_context():
            article = Article(
                id="test_article",
                title="Test Article",
                summary="This is a test article.",
                published_date="2024-01-27"
            )
            db.session.add(article)
            db.session.commit()

        with app.app_context():
            retrieved_article = db.session.get(Article, "test_article")
            self.assertIsNotNone(retrieved_article)
            self.assertEqual(retrieved_article.title, "Test Article")

    def test_author_model(self):
        # Test creating and querying an Author
        with app.app_context():
            article = Article(
                id="test_article",
                title="Test Article",
                summary="This is a test article.",
                published_date="2024-01-27"
            )
            author = Author(
                name="Test Author",
                affiliation="Test Affiliation",
                article=article
            )
            db.session.add(article)
            db.session.add(author)
            db.session.commit()

        with app.app_context():
            # Use Session.get() instead of Query.get()
            retrieved_author = db.session.get(Author, 1)
            self.assertIsNotNone(retrieved_author)
            self.assertEqual(retrieved_author.name, "Test Author")

if __name__ == '__main__':
    unittest.main()
