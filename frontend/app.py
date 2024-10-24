from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return render_template('index.html', error="Please provide a search term.")

    response = requests.get(f'http://backend:5000/search?q={query}')
    results = response.json()

    return render_template('index.html', query=query, results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

