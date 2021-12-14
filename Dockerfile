FROM gcr.io/uwit-mci-axdd/django-container:1.3.7 as app-prewebpack-container

USER root
RUN apt-get update && apt-get install libpq-dev -y
USER acait

ADD --chown=acait:acait pathways/VERSION /app/pathways/
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/

RUN . /app/bin/activate && pip install -r requirements.txt

RUN . /app/bin/activate && pip install psycopg2

#ADD --chown=acait:acait docker/app_start.sh /scripts
#RUN chmod u+x /scripts/app_start.sh

FROM node:14.18.1-stretch AS wpack

ADD ./package.json /app/
WORKDIR /app/
RUN npm install .

ADD . /app/

ARG VUE_DEVTOOLS
ENV VUE_DEVTOOLS=$VUE_DEVTOOLS
RUN npx webpack --mode=production

FROM app-prewebpack-container as app-container

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ project/
COPY --chown=acait:acait --from=wpack /app/pathways/static /static

RUN . /app/bin/activate && python manage.py collectstatic --noinput

RUN . /app/bin/activate && python manage.py migrate
RUN . /app/bin/activate && python manage.py import_data

FROM gcr.io/uwit-mci-axdd/django-test-container:1.3.7 as app-test-container

ENV NODE_PATH=/app/lib/node_modules
COPY --from=app-container /app/ /app/
COPY --from=app-container /static/ /static/
