from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_webpack import Webpack
from gevent.wsgi import WSGIServer
from random import randint
from controllers import *

import os

app = Flask(__name__)
webpack = Webpack()
app.config.update({ 'DEBUG': True, 'WEBPACK_MANIFEST_PATH': './build/manifest.json' })
webpack.init_app(app)


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
