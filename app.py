from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

NEWS_API_KEY = '70d6dc47696245029782e856a3c6b5ff'
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/notizie', methods=['GET'])
def get_news():
    paese = request.args.get('country', 'it')
    categoria = request.args.get('category', 'general')
    params = {
        'apiKey': NEWS_API_KEY,
        'country': paese,
        'category': categoria,
        'pageSize': 5,
    }
    response = requests.get(NEWS_API_URL, params=params)
    data = response.json()
    if data.get("status") != "ok":
        return jsonify({"error": "Errore nel recupero notizie"}), 500

    notizie = []
    for articolo in data.get('articles', []):
        notizie.append({
            'titolo': articolo['title'],
            'descrizione': articolo['description'],
            'url': articolo['url'],
            'fonte': articolo['source']['name'],
            'data': articolo['publishedAt']
        })
    return jsonify(notizie)

if __name__ == '__main__':
    app.run(debug=True)
