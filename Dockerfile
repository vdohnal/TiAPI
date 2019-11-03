FROM python:3.7.4-alpine

ENV PYTHONUNBUFFERED 1
ENV LIBRARY_PATH=/lib:/usr/lib

RUN mkdir /code/
WORKDIR /code/

COPY ./Pipfile /code/Pipfile
COPY ./Pipfile.lock /code/Pipfile.lock

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev postgresql-client \
    && pip install pipenv \
    && pipenv install --system --ignore-pipfile --deploy \
    && apk del build-deps

COPY . /code/

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]
