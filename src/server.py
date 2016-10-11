from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_webpack import Webpack
from gevent.wsgi import WSGIServer

import os

from elasticsearch import Elasticsearch

from search import build_search_query, build_es_search_body_request, \
    build_es_aggregation_body_request, format_search_results, \
    format_aggregation_results, build_autocomplete_search_body_request, \
    format_autocomplete_results


es = Elasticsearch(os.environ['ES_URI'], timeout=5, retry_on_timeout=False)
ES_INDEX = 'searchable_items_prototype'

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
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    category = request.args.get('category', '')
    sort_by = request.args.get('sort_by', '')

    category_filters = {
        "gene": ['go_ids', 'go_names'],
        "go": ['gene']
    }

    search_fields = ['name', 'symbol', 'synonym', 'go_ids', 'go_names']

    json_response_fields = ['name', 'symbol', 'synonym', 'go_ids',
                            'go_names', 'href', 'type', 'organism']

    es_query = build_search_query(query, search_fields, category,
                                  category_filters, request.args)

    search_body = build_es_search_body_request(query,
                                               category,
                                               es_query,
                                               json_response_fields,
                                               search_fields,
                                               sort_by)

    search_results = es.search(
        index=ES_INDEX,
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

    aggregation_body = build_es_aggregation_body_request(
        es_query,
        category,
        category_filters
    )

    aggregation_results = es.search(
        index=ES_INDEX,
        body=aggregation_body
    )

    response = {
        'total': search_results['hits']['total'],
        'results': format_search_results(search_results, json_response_fields),
        'aggregations': format_aggregation_results(
            aggregation_results,
            category,
            category_filters
        )
    }

    return jsonify(response)


@app.route('/api/search_autocomplete')
def search_autocomplete():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    field = request.args.get('field', 'name')

    if query == '':
        return jsonify({
            "results": None
        })

    autocomplete_results = es.search(
        index=ES_INDEX,
        body=build_autocomplete_search_body_request(query, category, field)
    )

    return jsonify({
        "results": format_autocomplete_results(autocomplete_results, field)
    })


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


if __name__ == '__main__':
    if os.environ.get('PRODUCTION', ''):
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
    else:
        app.run(debug=True)
