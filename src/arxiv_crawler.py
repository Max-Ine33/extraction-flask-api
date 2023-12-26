import feedparser
import requests

arxiv_api_feed_url = "http://export.arxiv.org/api/query"  # URL for the ArXiv API


def fetch_metadata_by_id(article_id):
    """Fetch metadata about an article using its id. Ex: cond-mat/0102536v1"""
    url_id = arxiv_api_feed_url + "?id_list=" + article_id
    # print(url_id)
    data = requests.get(url_id)
    my_feed = feedparser.parse(data.text)
    # print(data.text)
    return my_feed
    # print(len(my_feed['entries']))


def get_arxiv_articles(query="all", start=0, max_results=10):
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
    """Fetch summary of an article using its id. Ex: cond-mat/0102536v1"""
    url_id = arxiv_api_feed_url + "?id_list=" + article_id
    data = requests.get(url_id)
    my_feed = feedparser.parse(data.text)
    return my_feed["entries"][0]["summary"]
