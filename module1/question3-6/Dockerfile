FROM python:3.12.8

# install poetry
RUN apt-get update && pip install poetry==2.0.0

# specify work directory
WORKDIR /app

# copy poetry files
COPY ./README.md /app/README.md
COPY ./poetry.lock /app/poetry.lock
COPY ./pyproject.toml /app/pyproject.toml

RUN python -m venv /venv
ENV PATH=/venv/bin:$PATH VIRTUAL_ENV=/venv
RUN poetry install --sync --no-root

COPY dataset /app/dataset
COPY ingest_data.py /app/ingest_data.py 

ENTRYPOINT [ "python", "ingest_data.py" ]
