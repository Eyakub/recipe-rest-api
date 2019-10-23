FROM python:3.7-alpine
MAINTAINER eyakubsorkar

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps
RUN apk update
RUN mkdir /src
WORKDIR /src
COPY ./src /src

RUN adduser -D user
USER user

