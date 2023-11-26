from flask import Flask, jsonify, request
import arxiv_crawler

app = Flask(__name__)

@app.route("/")
def home():
    return 'Homepage lol'

@app.route('/articles', methods=['GET'])
def get_articles():
    '''Get all articles of arXiv. Can search articles by keyword with --> articles?search=keyword'''
    search = request.args.get('search')
    if search is None: # For now, not printing all the articles, need to specify keyword
        return jsonify({'error': 'Search keyword "search" is required'}), 400
    articles = arxiv_crawler.fetch_arxiv_data(search)
    return jsonify({'articles': articles})

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