FROM sunpeek/poetry:py3.12-slim

ARG ENVIRONMENT=production
ENV ENVIRONMENT=${ENVIRONMENT}

COPY pyproject.toml /opt/app/
COPY poetry.lock /opt/app/
COPY ./app ./app
COPY ./envs ./envs

RUN poetry install $(test "$ENVIRONMENT" != local && echo "--only main") --no-interaction --no-ansi
