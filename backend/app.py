from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
es = Elasticsearch(['http://elasticsearch:9200'])
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def get_relevant_results(query):
    # Search Elasticsearch for relevant documents
    search_results = es.search(index="egov_services", query={
        "match": {"main_content": query}
    })

    # Rank results with NLP
    query_embedding = model.encode(query, convert_to_tensor=True)
    ranked_results = []
    for result in search_results['hits']['hits']:
        content = result['_source']['main_content']
        content_embedding = model.encode(content, convert_to_tensor=True)
        score = util.pytorch_cos_sim(query_embedding, content_embedding).item()
        ranked_results.append((result['_source'], score))

    # Sort by relevance score
    ranked_results = sorted(ranked_results, key=lambda x: x[1], reverse=True)
    return [res[0] for res in ranked_results]

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    results = get_relevant_results(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

