# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "author"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    article_id = db.Column(db.String(255), db.ForeignKey("article.id", ondelete="CASCADE"), nullable=False)

    # Define the relationship with the Article model
    article = relationship("Article", back_populates="authors")


class Article(db.Model):
    __tablename__ = "article"

    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255))
    summary = db.Column(db.Text)
    published_date = db.Column(db.String(20))
    updated_date = db.Column(db.String(20))
    doi = db.Column(db.String(50))
    comment = db.Column(db.Text)
    journal_reference = db.Column(db.String(255))

    # Define the relationship with the Author model
    authors = relationship("Author", back_populates="article", cascade="all, delete-orphan", passive_deletes=True)
