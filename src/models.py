# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Article(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255))
    summary = db.Column(db.Text)
    published_date = db.Column(db.String(20))
    updated_date = db.Column(db.String(20))
    authors = db.relationship("Author", backref="article", lazy=True)
    doi = db.Column(db.String(50))
    comment = db.Column(db.Text)
    journal_reference = db.Column(db.String(255))


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    article_id = db.Column(db.String(255), db.ForeignKey("article.id"), nullable=False)
