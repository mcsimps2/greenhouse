# Dockerfile

FROM python:3.9.5-slim-buster


# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV PYTHONPATH /code/

# install psycopg2 dependencies
# add vim for debugging
RUN apt-get update -y \
    && apt-get install git -y \
    && apt-get install gcc musl-dev -y \
    && apt-get install libpq-dev postgresql-11 postgresql-server-dev-11 postgresql-contrib-11 -y \
    && apt-get install libssl-dev libffi-dev -y

# Set up poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"

# Install dependencies before copying all project files to support caching this step
# Otherwise, if any project file change and this step comes after the next, then it's not cached
COPY requirements-dev.txt requirements-dev.txt
RUN pip install -r requirements-dev.txt

# Work directory (put after pip install b/c mounting volume during dev might overwrite)
# https://stackoverflow.com/questions/29905909/pip-install-e-packages-dont-appear-in-docker
# TODO: update - unpack mediafiles/staticfiles to /app/..., /app/code, etc...
RUN mkdir /code/
WORKDIR /code/
COPY . /code/
