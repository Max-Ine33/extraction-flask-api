from flask import Flask, jsonify, request
import arxiv_crawler

app = Flask(__name__)

@app.route("/")
def home():
    return 'Homepage lol'


@app.route('/articles', methods=['GET'])
def get_articles():
    '''Get all articles of arXiv. Can search articles by keyword with --> articles?search=keyword'''
    page = int(request.args.get('page', 1))
    per_page = 10
    start = (page - 1) * per_page
    max_results = per_page
    search = request.args.get('search')

    articles = arxiv_crawler.get_arxiv_articles(query=search, start=start, max_results=max_results)

    if articles is not None:
        return jsonify({'articles': articles})
    else:
        return jsonify({'error': 'Failed to fetch articles from arXiv'}), 500


@app.route('/articles/<path:id>', methods=['GET']) # Used <path:> because there is a / in the id of an article
def get_articles_by_id(id):
    '''Get metadata on an article using its id'''
    metadata = arxiv_crawler.fetch_metadata_by_id(id)
    return metadata

@app.route('/text', methods=['GET'])
def get_summary():
    return 'still building that'


if __name__ == '__main__':
    app.run(debug=True) #Reload app when changes are made