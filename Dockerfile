FROM python:3.7-alpine
LABEL maintainer="Aleksey Nakoryakov"

RUN apk update \
    && apk add --virtual .build-dependencies g++ ccache \
    && apk add python-dev libffi-dev libressl-dev libxml2-dev libxslt-dev \
    && pip3 install --no-cache-dir spb-dnevnik-bot

ENTRYPOINT ["dnevnik-bot"]