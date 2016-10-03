from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_webpack import Webpack
from gevent.wsgi import WSGIServer

import os

from elasticsearch import Elasticsearch

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
    sort_by = request.args.get('sort_by', '')

    fields = ['name', 'symbol', 'synonym', 'go_ids', 'go_names', 'href', 'type']

    for special_char in ['-', '.']:
        if special_char in query:
            query = "\"" + query + "\""
            break

    if query is "":
        es_query = {
            "match_all": {}
        }
    else:
        es_query = {
            'dis_max': {
                'queries': [
                    {
                        "term": {
                            "name.simple": {
                                "value": query,
                                "boost": 100
                            }
                        }
                    },
                    {
                        "multi_match": {
                            "query": query,
                            "type": "most_fields",
                            "fields": fields + ['description', 'name.stemmed^2'],
                            "boost": 25
                        }
                    },
                    {
                        "match_phrase_prefix": {
                            "keys": {
                                "query": query,
                                "analyzer": "standard",
                                "max_expansions": 12,
                                "boost": 10
                            }
                        }
                    },
                    {
                        "match_phrase_prefix": {
                            "name": {
                                "query": query,
                                "analyzer": "standard",
                                "max_expansions": 30,
                                "boost": 1
                            }
                        }
                    }
                ]
            }
        }

        if query == '':
            results_search_body = {
                "query": {
                    "function_score": {
                        "query": es_query,
                        "random_score": {
                            "seed": 12345
                        }
                    }
                },
                'highlight': {
                    'fields': {}
                }
            }
        else:
            results_search_body = {
                'query': es_query,
                'highlight': {
                    'fields': {}
                }
            }

        if sort_by == 'alphabetical':
            results_search_body['sort'] = [
                {
                    "name.raw": {
                        "order": "asc"
                    }
                }
            ]

        highlight_fields = ['name', 'name.stemmed', 'name.simple', 'description'] + fields
        for field in highlight_fields:
            results_search_body['highlight']['fields'][field] = {}

        results_search_body['_source'] = fields

        search_results = es.search(index=SEARCH_ES_INDEX, body=results_search_body, size=limit, from_=offset)

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
