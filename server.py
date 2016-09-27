from flask import Flask, render_template
from flask_webpack import Webpack

webpack = Webpack()
app = Flask(__name__)

params = {
    'DEBUG': True,
    'WEBPACK_MANIFEST_PATH': './build/manifest.json',
    'WEBPACK_ASSETS_URL': '/scripts/'
}
app.config.update(params)
webpack.init_app(app)

@app.route('/')
def hello_world():
     return render_template('index.jinja2')
