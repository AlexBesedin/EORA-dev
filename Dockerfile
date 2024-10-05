
FROM python:3.11.9-slim

RUN mkdir /eora-dev

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

WORKDIR /eora-dev

COPY ./pyproject.toml ./
RUN poetry install --no-root

COPY . .

WORKDIR /eora-dev/src
CMD poetry run python main.py
