# app.py
import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Article, Author
from utils import article_to_dict, fetch_summary_by_id, populate_single_article, populate_articles_by_query, get_arxiv_articles
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(os.getcwd(), "data/arxiv_articles.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    # Initialize the database
    db.create_all()

    @app.route("/")
    def home():
        return "Homepage"

    @app.route("/articles", methods=["POST"])
    def upload_new_article():
        data = request.get_json()

        new_article = Article(
            id=data.get("id"),
            title=data.get("title"),
            summary=data.get("summary"),
            published_date=data.get("published_date"),
            updated_date=data.get("updated_date"),
            doi=data.get("doi"),
            comment=data.get("comment"),
            journal_reference=data.get("journal_reference")
        )

        db.session.merge(new_article)
        db.session.commit()

        return jsonify({"document_id": new_article.id})



    @app.route("/articles", methods=["GET"], strict_slashes=False)
    def get_articles():
        query = request.args.get("query", "all")
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        start_date_str = request.args.get("start_date")
        end_date_str = request.args.get("end_date")
        subcategory = request.args.get("subcategory")

        # Parse start and end date strings to datetime objects if provided
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None

        # Base query
        articles_query = Article.query

        # Apply additional filters
        if query != "all":
            articles_query = articles_query.filter(Article.title.ilike(f"%{query}%"))
        if start_date:
            articles_query = articles_query.filter(Article.published_date >= start_date)
        if end_date:
            articles_query = articles_query.filter(Article.published_date <= end_date)
        if subcategory:
            articles_query = articles_query.filter(Article.subcategory == subcategory)

        # Paginate the results
        articles = articles_query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({"articles": [article_to_dict(article) for article in articles.items]})



    @app.route("/articles/<string:article_id>", methods=["GET"], strict_slashes=False)
    def get_article(article_id):
        """Describe the requested article, all metadata."""
        article = db.session.query(Article).filter_by(id=article_id).one_or_none()

        if article:
            return jsonify({"article": article_to_dict(article)})
        else:
            # If article not found in the database, fetch it from arXiv API
            articles = get_arxiv_articles(query=article_id, max_results=1)

            if articles:
                entry = articles[0]

                new_article = Article(
                    id=article_id,
                    title=entry.get("title", ""),
                    summary=entry.get("summary", ""),
                    published_date=entry.get("published_date", ""),
                    updated_date=entry.get("updated_date", ""),
                    doi=entry.get("doi", ""),
                    comment=entry.get("comment", ""),
                    journal_reference=entry.get("journal_reference", "")
                )

                # Add authors to the new article
                for author_entry in entry.get("authors", []):
                    author = Author(
                        name=author_entry.get("name", ""),
                        affiliation=author_entry.get("affiliation", ""),
                        article=new_article
                    )
                    db.session.add(author)

                # Add the new article to the database
                db.session.add(new_article)
                db.session.commit()

                return jsonify({"article": article_to_dict(new_article)})
            else:
                return jsonify({"error": "Article not found in arXiv"}), 404



    @app.route("/text/<string:article_id>", methods=["GET"], strict_slashes=False)
    def get_summary(article_id):
        summary = fetch_summary_by_id(article_id)
        return summary

    @app.route("/populate_articles", methods=["POST"], strict_slashes=False)
    def populate_articles():
        data = request.get_json()

        article_id = data.get("article_id")
        query = data.get("query", "all")
        max_results = data.get("max_results", 10)

        if article_id:
            return populate_single_article(article_id)
        else:
            return populate_articles_by_query(query, max_results)

if __name__ == "__main__":
    app.run(debug=True)
