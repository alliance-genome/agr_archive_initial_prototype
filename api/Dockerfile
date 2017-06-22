FROM flask_server_env:latest

WORKDIR /app

ADD . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN nosetests -s test

WORKDIR /app/src

CMD gunicorn server:app -b 0.0.0.0:5000 --access-logfile=- --error-logfile=-
