# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Article(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255))
    summary = db.Column(db.Text)
    published_date = db.Column(db.String(20))
    # Add other columns as needed
