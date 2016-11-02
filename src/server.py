from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_webpack import Webpack
from gevent.wsgi import WSGIServer
from random import randint

import os

from elasticsearch import Elasticsearch

from search import build_search_query, build_es_search_body_request, \
    build_es_aggregation_body_request, format_search_results, \
    format_aggregation_results, build_autocomplete_search_body_request, \
    format_autocomplete_results


es = Elasticsearch(os.environ['ES_URI'], timeout=5, retry_on_timeout=False)
ES_INDEX = 'searchable_items_blue'

app = Flask(__name__)

webpack = Webpack()
params = {
    'DEBUG': True,
    'WEBPACK_MANIFEST_PATH': './build/manifest.json'
}

app.config.update(params)
webpack.init_app(app)

# TEMP
@app.route('/api/graph_search')
def graph_search():
    MAX_COORD = 100000
    SPECIES = [
        {
            'name': 'Homo sapiens',
            'chromosomes': [
                500000,
                100000,
                1000000,
                1200000
            ]
        },
        {
            'name': 'Mus musculus',
            'chromosomes': [
                100000,
                200000,
                1200000,
                40000
            ]
        },
        {
            'name': 'Danio rerio',
            'chromosomes': [
                50000,
                1200000,
                100000
            ]
        },
                {
            'name': 'Drosophila melanogaster',
            'chromosomes': [
                50000,
                1200000,
                100000
            ]
        }
    ]

    # pick random number rn 100 - 800
    rn = randint(25, 1000)
    # make rn nodes with random species
    nodes = []
    print rn
    for i in xrange(rn):
        new_node = {
            'name': 'abc' + str(i),
            'id': i,
            'species': SPECIES[randint(0, len(SPECIES) - 1)]['name'],
            'start': randint(0, MAX_COORD)
        }
        nodes.append(new_node)
    # pick random number rl less than that for links
    rl = randint(25, rn)
    # make rl links to random places
    edges = []
    for _ in xrange(rl):
        random_source = nodes[randint(0, len(nodes) - 1)]
        random_target = nodes[randint(0, len(nodes) - 1)]
        new_edge = { 'source': random_source['id'], 'target': random_target['id'] }
        edges.append(new_edge)
    
    graph_data = { 'nodes': nodes, 'edges': edges, 'meta': SPECIES }
    return jsonify(graph_data)

@app.route('/api/search')
def search():
    query = request.args.get('q', '').lower()
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    category = request.args.get('category', '')
    sort_by = request.args.get('sort_by', '')

    category_filters = {
        "gene": ['gene_type', 'gene_biological_process', 'gene_molecular_function', 'gene_cellular_component', 'species'],
        "go": ['go_type', 'go_species', 'go_genes'],
        "disease": ['disease_species', 'disease_genes']
    }

    search_fields = ['name', 'gene_symbol', 'gene_synonyms', 'description', 'external_ids', 'species', 'gene_biological_process', 'gene_molecular_function', 'gene_cellular_component', 'go_type', 'go_genes', 'disease_genes']

    json_response_fields = ['name', 'gene_symbol', 'gene_synonyms', 'gene_type', 'gene_chromosomes','gene_chromosome_starts', 'gene_chromosome_ends', 'description', 'external_ids', 'species', 'gene_biological_process', 'gene_molecular_function', 'gene_cellular_component', 'go_type', 'go_genes', 'disease_genes', 'homologs', 'category', 'href']

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
        from_=offset,
        preference='p_'+query
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
    field = request.args.get('field', 'name_key')

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
