import requests
import feedparser

arxiv_api_feed_url = "http://export.arxiv.org/api/query" # URL for the ArXiv API

def fetch_arxiv_data(query):
    '''Fetch 10 articles for a certain keyword'''
    params = {'search_query': query, 'max_results': 10}
    response = requests.get(arxiv_api_feed_url, params=params)
    feed = feedparser.parse(response.text)
    entries = feed.entries
    return entries

def fetch_metadata_by_id(article_id):
    ''' Fetch metadata about an article by using its id. Ex: cond-mat/0102536v1'''
    url_id = arxiv_api_feed_url + '?id_list=' + article_id
    # print(url_id)
    data = requests.get(url_id)
    my_feed = feedparser.parse(data.text)
    # print(data.text)
    return my_feed
    #print(len(my_feed['entries']))
