# app.py
import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Article
from utils import article_to_dict, fetch_summary_by_id, populate_single_article, populate_articles_by_query

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(os.getcwd(), "data/arxiv_articles.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    # Initialize the database
    db.create_all()

    @app.route("/")
    def home():
        return "Homepage lol"

    @app.route("/articles", methods=["POST"])
    def upload_new_article():
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
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))

        articles = Article.query.paginate(page=page, per_page=per_page, error_out=False)
        return jsonify({"articles": [article_to_dict(article) for article in articles.items]})

    @app.route("/articles/<string:article_id>", methods=["GET"])
    def get_article(article_id):
        article = Article.query.get(article_id)
        if article:
            return jsonify({"article": article_to_dict(article)})
        else:
            return jsonify({"error": "Article not found"}), 404

    @app.route("/text/<string:article_id>", methods=["GET"])
    def get_summary(article_id):
        summary = fetch_summary_by_id(article_id)
        return summary

    @app.route("/populate_articles", methods=["POST"])
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
