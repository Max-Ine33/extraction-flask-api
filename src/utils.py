# utils.py
import feedparser
import requests
from models import db, Article, Author
from flask import jsonify

# ArXiv API URL
ARXIV_API_FEED_URL = "http://export.arxiv.org/api/query"

def article_to_dict(article):
    return {
        "id": article.id,
        "title": article.title,
        "summary": article.summary,
        "published_date": article.published_date,
        "updated_date": article.updated_date,
        "doi": article.doi,
        "comment": article.comment,
        "journal_reference": article.journal_reference,
        "authors": [
            {"name": author.name, "affiliation": author.affiliation}
            for author in article.authors
        ],
        # Add other fields as needed
    }


def fetch_metadata_by_id(article_id):
    url_id = ARXIV_API_FEED_URL + "?id_list=" + article_id
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

    response = requests.get(ARXIV_API_FEED_URL, params=params)
    feed = feedparser.parse(response.text)
    entries = feed.entries

    articles = []
    for entry in entries:
        article_id = entry.get("id", "").split("/")[-1]
        summary = entry.get("summary", "")
        published_date = entry.get("published", "")
        updated_date = entry.get("updated", "")
        doi = entry.get("arxiv_doi", "")
        comment = entry.get("arxiv_comment", "")
        journal_reference = entry.get("arxiv_journal_ref", "")

        # Extract authors and affiliations
        authors = []
        for author_entry in entry.get("authors", []):
            author_name = author_entry.get("name", "")
            authors.append({
                "name": author_name
            })

        articles.append({
            "id": article_id,
            "title": entry.get("title", ""),
            "summary": summary,
            "published_date": published_date,
            "updated_date": updated_date,
            "doi": doi,
            "comment": comment,
            "journal_reference": journal_reference,
            "authors": authors,
        })

    return articles





def fetch_summary_by_id(article_id):
    url_id = ARXIV_API_FEED_URL + "?id_list=" + str(article_id)
    data = requests.get(url_id)
    my_feed = feedparser.parse(data.text)

    if "entries" in my_feed and my_feed["entries"]:
        return my_feed["entries"][0]["summary"]
    else:
        return "Summary not available"


def populate_single_article(article_id):
    existing_article = Article.query.get(article_id)

    if existing_article is None:
        # Fetch article details from arXiv API
        url_id = ARXIV_API_FEED_URL + "?id_list=" + article_id
        data = requests.get(url_id)
        my_feed = feedparser.parse(data.text)

        if "entries" in my_feed and my_feed["entries"]:
            entry = my_feed["entries"][0]

            new_article = Article(
                id=article_id,
                title=entry.get("title", ""),
                summary=entry.get("summary", ""),
                published_date=entry.get("published", ""),
                updated_date=entry.get("updated", ""),
                doi=entry.get("arxiv_doi", ""),
                comment=entry.get("arxiv_comment", ""),
                journal_reference=entry.get("arxiv_journal_ref", "")
            )

            # Add authors to the new article
            for author_entry in entry.get("authors", []):
                author = Author(
                    name=author_entry.get("name", ""),
                    affiliation=author_entry.get("arxiv_affiliation", ""),
                    article=new_article
                )
                db.session.add(author)

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

    articles = get_arxiv_articles(query=query, max_results=max_results)

    for entry in articles:
        article_id = entry["id"]
        existing_article = Article.query.get(article_id)

        if existing_article is None:
            new_article = Article(
                id=article_id,
                title=entry["title"],
                summary=entry["summary"],
                published_date=entry["published_date"],
                updated_date=entry["updated_date"],
                doi=entry["doi"],
                comment=entry["comment"],
                journal_reference=entry["journal_reference"]
            )

            # Add authors to the new article
            for author_entry in entry.get("authors", []):
                author = Author(
                    name=author_entry.get("name", ""),
                    affiliation=author_entry.get("affiliation", ""),
                    article=new_article
                )
                db.session.add(author)

            db.session.add(new_article)

    db.session.commit()

    return jsonify({"message": "Articles added to the database successfully"})


