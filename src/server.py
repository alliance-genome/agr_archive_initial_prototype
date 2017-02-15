from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_webpack import Webpack
from gevent.wsgi import WSGIServer
from random import randint

import os

from awses.connection import AWSConnection
from elasticsearch import Elasticsearch

from controllers.helpers import build_search_query, build_es_search_body_request, \
    build_es_aggregation_body_request, format_search_results, \
    format_aggregation_results, build_autocomplete_search_body_request, \
    format_autocomplete_results

es = Elasticsearch(connection_class=AWSConnection,
                   region='us-west-2',
                   host=os.environ['ES_URI'], timeout=5, retry_on_timeout=False) if os.environ['ES_AWS'] == "true" else Elasticsearch(os.environ['ES_URI'], timeout=5, retry_on_timeout=False)

ES_INDEX = os.environ['ES_INDEX']

app = Flask(__name__)
webpack = Webpack()
app.config.update({ 'DEBUG': True, 'WEBPACK_MANIFEST_PATH': './build/manifest.json' })
webpack.init_app(app)

from controllers import *

controllers = {
	"disease": DiseaseController(),
	"gene": GeneController(),
	"go": GoController(),
	"search": SearchController(),
}

# Search
@app.route('/api/search')
def search():
    controller_c = controllers["search"]

    query = request.args.get('q', '')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    category = request.args.get('category', '')
    sort_by = request.args.get('sort_by', '')

    return jsonify(controller_c.search(query, limit, offset, category, sort_by, request.args))

# Search Auto Complete
@app.route('/api/search_autocomplete')
def search_autocomplete():
    controller_c = controllers["search"]

    query = request.args.get('q', '')
    category = request.args.get('category', '')
    field = request.args.get('field', 'name_key')

    return jsonify(controller_c.autocomplete(query, category, field))

# Create
@app.route('/api/<controller>', methods=['POST'])
def gene_create_api(controller):
    controller_c = controllers[controller]
    object = request.get_json()
    return jsonify(controller_c.create(object))

# Read
@app.route('/api/<controller>/<id>', methods=['GET'])
def read_api(controller, id):
    controller_c = controllers[controller]
    return jsonify(controller_c.get(id)['_source'])

# Update
@app.route('/api/<controller>/<id>', methods=['PUT'])
def gene_update_api(controller, id):
    controller_c = controllers[controller]
    object = request.get_json()
    return jsonify(controller_c.save(id, object))

# Delete
@app.route('/api/<controller>/<id>', methods=['DELETE'])
def gene_delete_api(controller, id):
    controller_c = controllers[controller]
    return jsonify(controller_c.delete(id))


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

if __name__ == '__main__':
    if os.environ.get('PRODUCTION', ''):
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
    elif os.environ.get('DOCKER', ''):
        app.run(host='0.0.0.0', debug=True)
    else:
        app.run(debug=True)
