from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import feedparser
import requests
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///arxiv_articles.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

with app.app_context():
    # Initialize the database
    db.create_all()

    class Article(db.Model):
        id = db.Column(db.String(255), primary_key=True)
        title = db.Column(db.String(255))
        summary = db.Column(db.Text)
        published_date = db.Column(db.String(20))
        # Add other columns as needed

    # ArXiv API URL
    arxiv_api_feed_url = "http://export.arxiv.org/api/query"

    def article_to_dict(article):
        return {
            "id": article.id,
            "title": article.title,
            "summary": article.summary,
            "published_date": article.published_date,
            # Add other fields as needed
        }

    def fetch_metadata_by_id(article_id):
        """Fetch metadata about an article using its id."""
        url_id = arxiv_api_feed_url + "?id_list=" + article_id
        data = requests.get(url_id)
        my_feed = feedparser.parse(data.text)
        return my_feed

    def get_arxiv_articles(query="all", start=0, max_results=10):
        """Get ArXiv articles based on the search query."""
        if not query or query.strip() == "":
            query = "all"

        params = {
            "search_query": query,
            "start": start,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }

        response = requests.get(arxiv_api_feed_url, params=params)
        feed = feedparser.parse(response.text)
        entries = feed.entries
        return entries

    def fetch_summary_by_id(article_id):
        """Fetch summary of an article using its id."""
        url_id = arxiv_api_feed_url + "?id_list=" + str(article_id)
        data = requests.get(url_id)
        my_feed = feedparser.parse(data.text)

        if "entries" in my_feed and my_feed["entries"]:
            return my_feed["entries"][0]["summary"]
        else:
            return "Summary not available"



    # Initialize the database
    db.create_all()

    with app.app_context():
        @app.route("/")
        def home():
            return "Homepage lol"

        @app.route("/articles", methods=["POST"])
        def upload_new_article():
            """Upload a new article and respond with a document ID."""
            data = request.get_json()

            new_article = Article(
                id=data.get("id"),
                title=data.get("title"),
                summary=data.get("summary"),
                published_date=data.get("published_date")
            )

            db.session.merge(new_article)
            db.session.commit()

            return jsonify({"document_id": new_article.id})

        @app.route("/articles", methods=["GET"])
        def get_all_articles():
            """List all articles, preferably paginated."""
            page = int(request.args.get("page", 1))
            per_page = int(request.args.get("per_page", 10))

            articles = Article.query.paginate(page=page, per_page=per_page, error_out=False)
            return jsonify({"articles": [article_to_dict(article) for article in articles.items]})

        @app.route("/articles/<string:article_id>", methods=["GET"])
        def get_article(article_id):
            """Describe the requested article, all metadata."""
            article = Article.query.get(article_id)
            if article:
                return jsonify({"article": article_to_dict(article)})
            else:
                return jsonify({"error": "Article not found"}), 404

        @app.route("/text/<string:article_id>", methods=["GET"])
        def get_summary(article_id):
            """Get the summary of an article using its id."""
            summary = fetch_summary_by_id(article_id)
            return summary
        
        @app.route("/populate_articles", methods=["POST"])
        def populate_articles():
            """Fetch articles from arXiv API and add them to the database."""
            data = request.get_json()

            article_id = data.get("article_id")
            query = data.get("query", "all")
            max_results = data.get("max_results", 10)

            if article_id:
                # Populate a single article by ID
                return populate_single_article(article_id)
            else:
                # Populate articles based on query and max_results
                return populate_articles_by_query(query, max_results)

        def populate_single_article(article_id):
            existing_article = Article.query.get(article_id)

            if existing_article is None:
                # Fetch article details from arXiv API
                url_id = arxiv_api_feed_url + "?id_list=" + article_id
                data = requests.get(url_id)
                my_feed = feedparser.parse(data.text)

                if "entries" in my_feed and my_feed["entries"]:
                    entry = my_feed["entries"][0]

                    new_article = Article(
                        id=article_id,
                        title=entry.get("title", ""),
                        summary=entry.get("summary", ""),
                        published_date=entry.get("published", "")
                    )

                    # Add the new article to the database
                    db.session.add(new_article)
                    db.session.commit()

                    return jsonify({"message": "Article added to the database successfully"})
                else:
                    return jsonify({"error": "Article not found in arXiv"}), 404
            else:
                return jsonify({"error": "Article already exists in the database"}), 400

        def populate_articles_by_query(query, max_results):
            # Implement logic to populate articles based on query and max_results
            # You can use your existing logic from the get_arxiv_articles function

            articles = get_arxiv_articles(query=query, max_results=max_results)

            for entry in articles:
                article_id = entry.id.split("/")[-1]
                existing_article = Article.query.get(article_id)

                if existing_article is None:
                    new_article = Article(
                        id=article_id,
                        title=entry.title,
                        summary=entry.summary,
                        published_date=entry.published
                    )
                    db.session.add(new_article)

            db.session.commit()

            return jsonify({"message": "Articles added to the database successfully"})  
        

if __name__ == "__main__":
    app.run(debug=True)
