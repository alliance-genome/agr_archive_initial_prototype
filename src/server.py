from flask import Flask, render_template, send_from_directory
from flask_webpack import Webpack

app = Flask(__name__)

# prepare to get asset URLs from manifest.json and use flask_webpack plugin
webpack = Webpack()
params = {
    'DEBUG': True,
    'WEBPACK_MANIFEST_PATH': './build/manifest.json'
}
app.config.update(params)
webpack.init_app(app)

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
