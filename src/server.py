from flask import Flask, render_template, send_from_directory
from flask_webpack import Webpack

use_webpack = True

app = Flask(__name__)

if (use_webpack):
	webpack = Webpack()
	params = {
	    'DEBUG': True,
	    'WEBPACK_MANIFEST_PATH': './build/manifest.json'
	}
	app.config.update(params)
	webpack.init_app(app)
else:
	@app.route('/assets/<path:path>')
	def send_static(path):
		return send_from_directory('build', path)

@app.route('/')
def react_render():
     return render_template('index.jinja2', use_webpack=use_webpack )
