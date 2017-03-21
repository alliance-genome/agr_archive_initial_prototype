from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_webpack import Webpack
from gevent.wsgi import WSGIServer
from random import randint
from services import *

import os

app = Flask(__name__)
webpack = Webpack()
app.config.update({ 'DEBUG': True, 'WEBPACK_MANIFEST_PATH': './build/manifest.json' })
webpack.init_app(app)
auth = HTTPBasicAuth()

services = {
	"disease": DiseaseService(),
	"gene": GeneService(),
	"go": GoService(),
	"search": SearchService(),
}

## Search
@app.route('/api/search')
def search():
   service_c = services["search"]
   query = request.args.get('q', '')
   limit = int(request.args.get('limit', 10))
   offset = int(request.args.get('offset', 0))
   category = request.args.get('category', '')
   sort_by = request.args.get('sort_by', '')
   return jsonify(service_c.search(query, limit, offset, category, sort_by, request.args))

## Search Auto Complete
@app.route('/api/search_autocomplete')
def search_autocomplete():
   service_c = services["search"]
   query = request.args.get('q', '')
   category = request.args.get('category', '')
   field = request.args.get('field', 'name_key')
   return jsonify(service_c.autocomplete(query, category, field))

# Create
@app.route('/api/<service>', methods=['POST'])
@auth.login_required
def gene_create_api(service):
    service_c = services[service]
    object = request.get_json()
    return jsonify(service_c.create(object))

# Read
@app.route('/api/<service>/<id>', methods=['GET'])
def read_api(service, id):
    service_c = services[service]
    return jsonify(service_c.get(id)['_source'])

# Update
@app.route('/api/<service>/<id>', methods=['PUT'])
@auth.login_required
def gene_update_api(service, id):
    service_c = services[service]
    object = request.get_json()
    return jsonify(service_c.save(id, object))

# Delete
@app.route('/api/<service>/<id>', methods=['DELETE'])
@auth.login_required
def gene_delete_api(service, id):
    service_c = services[service]
    return jsonify(service_c.delete(id))


# make static assets available
@app.route('/assets/<path:path>')
def send_static(path):
    return send_from_directory('build', path)

# render user interfaces in client JS
@app.route('/')
@app.route('/about')
@app.route('/help')
@app.route('/search')
@app.route('/gene/<gene_id>')
def react_render(gene_id = None):
    return render_template('index.jinja2')

@auth.get_password
def get_pw(username):
	print "Username: " + username
	return os.environ['API_PASSWORD']

if __name__ == '__main__':
    if os.environ.get('PRODUCTION', ''):
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
    elif os.environ.get('DOCKER', ''):
        app.run(host='0.0.0.0', debug=True)
    else:
        app.run(debug=True)

from services.helpers.search_helper import *

from elasticsearch import Elasticsearch
es = Elasticsearch(os.environ['ES_HOST'], timeout=5, retry_on_timeout=False)
ES_INDEX = os.environ['ES_INDEX']

# @app.route('/api/search')
# def search():
#     query = request.args.get('q', '')
#     limit = int(request.args.get('limit', 10))
#     offset = int(request.args.get('offset', 0))
#     category = request.args.get('category', '')
#     sort_by = request.args.get('sort_by', '')

#     category_filters = {
#         "gene": ['soTermName', 'gene_biological_process', 'gene_molecular_function', 'gene_cellular_component', 'species'],
#         "go": ['go_type', 'go_species', 'go_genes'],
#         "disease": ['disease_species', 'disease_genes']
#     }

#     search_fields = ['primaryId', 'name', 'symbol', 'symbol.raw', 'synonyms', 'synonyms.raw', 'description',
#                      'external_ids', 'species', 'gene_biological_process', 'gene_molecular_function',
#                      'gene_cellular_component', 'go_type', 'go_genes', 'go_synonyms', 'disease_genes',
#                      'disease_synonyms']

#     json_response_fields = ['name', 'symbol', 'synonyms', 'soTermName', 'gene_chromosomes', 'gene_chromosome_starts',
#                             'gene_chromosome_ends', 'description', 'external_ids', 'species',
#                             'gene_biological_process', 'gene_molecular_function', 'gene_cellular_component',
#                             'go_type', 'go_genes', 'go_synonyms', 'disease_genes', 'disease_synonyms', 'homologs',
#                             'crossReferences', 'category', 'href']


#     es_query = build_search_query(query, search_fields, category,
#                                   category_filters, request.args)

#     search_body = build_es_search_body_request(query,
#                                                category,
#                                                es_query,
#                                                json_response_fields,
#                                                search_fields,
#                                                sort_by)

#     search_results = es.search(
#         index=ES_INDEX,
#         body=search_body,
#         size=limit,
#         from_=offset,
#         preference='p_'+query
#     )

#     if search_results['hits']['total'] == 0:
#         return jsonify({
#             'total': 0,
#             'results': [],
#             'aggregations': []
#         })

#     aggregation_body = build_es_aggregation_body_request(
#         es_query,
#         category,
#         category_filters
#     )

#     aggregation_results = es.search(
#         index=ES_INDEX,
#         body=aggregation_body
#     )

#     response = {
#         'total': search_results['hits']['total'],
#         'results': format_search_results(search_results, json_response_fields),
#         'aggregations': format_aggregation_results(
#             aggregation_results,
#             category,
#             category_filters
#         )
#     }

#     return jsonify(response)


# @app.route('/api/search_autocomplete')
# def search_autocomplete():
#     query = request.args.get('q', '')
#     category = request.args.get('category', '')
#     field = request.args.get('field', 'name_key')

#     if query == '':
#         return jsonify({
#             "results": None
#         })

#     autocomplete_results = es.search(
#         index=ES_INDEX,
#         body=build_autocomplete_search_body_request(query, category, field)
#     )

#     return jsonify({
#         "results": format_autocomplete_results(autocomplete_results, field)
#     })

