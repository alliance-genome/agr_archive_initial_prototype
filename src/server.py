import os

from app import app

if __name__ == '__main__':
    if os.environ.get('PRODUCTION', ''):
        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()
    elif os.environ.get('DOCKER', ''):
        app.run(host='0.0.0.0', debug=True)
    else:
        app.run(debug=True)
