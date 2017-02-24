from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_webpack import Webpack
from flask_sqlalchemy import SQLAlchemy
from gevent.wsgi import WSGIServer
from random import randint
from services import *

import os

app = Flask(__name__)
app.config.update({ 'DEBUG': True, 'WEBPACK_MANIFEST_PATH': './build/manifest.json' })
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

webpack = Webpack()
webpack.init_app(app)
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

services = {
	"disease": DiseaseService(),
	"gene": GeneService(),
	"go": GoService(),
	"search": SearchService(),
}

# Search
@app.route('/api/search')
def search():
    service_c = services["search"]

    query = request.args.get('q', '')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    category = request.args.get('category', '')
    sort_by = request.args.get('sort_by', '')

    return jsonify(service_c.search(query, limit, offset, category, sort_by, request.args))

# Search Auto Complete
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
