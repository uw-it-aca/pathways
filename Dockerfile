ARG DJANGO_CONTAINER_VERSION=3.0.2

FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-container:${DJANGO_CONTAINER_VERSION} AS app-prebundler-container

USER root

RUN apt-get update && apt-get install python3-dev libpq-dev -y

USER acait

COPY --chown=acait:acait . /app/
COPY --chown=acait:acait docker/ /app/project/

COPY --chown=acait:acait docker/app_start.sh /scripts
RUN chmod u+x /scripts/app_start.sh

RUN /app/bin/pip install -r requirements.txt
RUN /app/bin/pip install "psycopg[c,pool]"

# latest node + ubuntu
FROM node:24 AS node-base
FROM ubuntu:24.04 AS node-bundler
COPY --from=node-base / /

COPY ./package.json /app/
WORKDIR /app/
RUN npm install .

COPY . /app/

ARG VUE_DEVTOOLS
ENV VUE_DEVTOOLS=$VUE_DEVTOOLS
RUN npm run build

FROM app-prebundler-container AS app-container

COPY --chown=acait:acait --from=node-bundler /app/pathways/static /app/pathways/static

RUN . /app/bin/activate && python manage.py collectstatic --noinput

FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-test-container:${DJANGO_CONTAINER_VERSION} AS app-test-container

ENV NODE_PATH=/app/lib/node_modules
COPY --from=app-container /app/ /app/
COPY --from=app-container /static/ /static/
