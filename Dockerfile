FROM decibel/uwsgi-nginx-flask-docker:python3.6-alpine3.8-pandas
MAINTAINER Giuseppe Broccolo <gbroccolo@decibelinsight.com>

RUN mkdir -p /source

COPY . /source
COPY ./main.py /app/
COPY ./uwsgi_flask_nginx/uwsgi_timeout.conf /etc/nginx/conf.d/
COPY ./uwsgi_flask_nginx/nginx.conf /etc/nginx/
COPY ./supervisord/supervisord.ini /etc/supervisor.d/

RUN cd /source &&\
    pip install --no-cache-dir . &&\
    cd / &&\
    rm -rf /source
