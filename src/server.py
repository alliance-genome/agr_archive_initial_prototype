from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_webpack import Webpack
from gevent.wsgi import WSGIServer

import os

from elasticsearch import Elasticsearch

from search import build_search_query, build_es_search_body_request

es = Elasticsearch(os.environ['ES_URI'], timeout=5, retry_on_timeout=True)
SEARCH_ES_INDEX = 'searchable_items_prototype'

app = Flask(__name__)

webpack = Webpack()
params = {
    'DEBUG': True,
    'WEBPACK_MANIFEST_PATH': './build/manifest.json'
}

app.config.update(params)
webpack.init_app(app)


@app.route('/api/search')
def search():
    query = request.args.get('q', '')
    limit = request.args.get('limit', 10)
    offset = request.args.get('offset', 0)
    category = request.args.get('category', '')
    sort_by = request.args.get('sort_by', '')

    category_filters = {
        "genes": ['go_ids', 'go_names'],
        "go": ['gene'],
    }

    search_fields = ['name', 'symbol', 'synonym', 'go_ids', 'go_names']

    json_response_fields = ['name', 'symbol', 'synonym', 'go_ids',
                            'go_names', 'href', 'type', 'organism']

    es_query = build_search_query(query, search_fields, category,
                                  category_filters, request)

    search_body = build_es_search_body_request(query,
                                               category,
                                               es_query,
                                               json_response_fields,
                                               search_fields,
                                               sort_by)

    search_results = es.search(
        index=SEARCH_ES_INDEX,
        body=search_body,
        size=limit,
        from_=offset
    )

    if search_results['hits']['total'] == 0:
        return jsonify({
            'total': 0,
            'results': [],
            'aggregations': []
        })

    response = {
        'total': search_results['hits']['total'],
        'results': []
    }

    for result in search_results['hits']['hits']:
        response['results'].append({
            'name': result['_source']['name'],
            'symbol': result['_source']['symbol'],
            'synonym': result['_source']['synonym'],
            'go_ids': result['_source']['go_ids'],
            'type': result['_source']['type'],
            'organism': result['_source']['organism'],
            'highlight': result['highlight']
        })

    return jsonify(response)


# make static assets available anyway
@app.route('/assets/<path:path>')
def send_static(path):
    return send_from_directory('build', path)


# render user interfaces in client JS
@app.route('/')
@app.route('/about')
@app.route('/help')
@app.route('/search')
def react_render():
        return render_template('index.jinja2')

if os.environ.get('PRODUCTION', ''):
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
else:
    app.run(debug=True)
