from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_webpack import Webpack
from flask_sqlalchemy import SQLAlchemy
from gevent.wsgi import WSGIServer
from random import randint
from services import *
from config import *

import os

if "PRODUCTION" in os.environ and os.environ['PRODUCTION']:
    config = ProductionConfig()
else:
    config = DevelopmentConfig()

app = Flask(__name__)
app.config.from_object(config)

webpack = Webpack()
webpack.init_app(app)
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

services = {
    "disease": DiseaseService(db),
    "gene": GeneService(db),
    "go": GoService(db),
    "so_term": SoTermService(db),
    "search": SearchService(app),
}

# Search
@app.route('/api/search')
def search():
    service = services["search"]

    query = request.args.get('q', '')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    category = request.args.get('category', '')
    sort_by = request.args.get('sort_by', '')

    return jsonify(service.search(query, limit, offset, category, sort_by, request.args))

# Search Auto Complete
@app.route('/api/search_autocomplete')
def search_autocomplete():
    service = services["search"]

    query = request.args.get('q', '')
    category = request.args.get('category', '')
    field = request.args.get('field', 'name_key')

    return jsonify(service.autocomplete(query, category, field))

# Create
@app.route('/api/<service>', methods=['POST'])
@auth.login_required
def create_api(service):
    service = services[service]
    object = request.get_json()
    return jsonify(service.create(object))

# Read
@app.route('/api/<service>/<id>', methods=['GET'])
def read_api(service, id):
    service = services[service]
    return jsonify(service.get(id)['_source'])

# Update
@app.route('/api/<service>/<id>', methods=['PUT'])
@auth.login_required
def update_api(service, id):
    service = services[service]
    object = request.get_json()
    return jsonify(service.save(id, object))

# Delete
@app.route('/api/<service>/<id>', methods=['DELETE'])
@auth.login_required
def delete_api(service, id):
    service = services[service]
    return jsonify(service.delete(id))


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
    return app.config['API_PASSWORD']

