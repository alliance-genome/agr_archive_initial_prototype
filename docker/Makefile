all: flask_env flask

flask_env:
	docker build -t flask_server - < docker/Dockerfile

flask:
	docker build -t flask_server_env - < Dockerfile-flask_server 
