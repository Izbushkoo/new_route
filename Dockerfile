FROM python:3.10-buster
LABEL authors="Izbushko"

RUN pip install poetry==1.6.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md
RUN apt-get update -y
RUN apt-get install -y ffmpeg portaudio19-dev libavcodec-extra libasound2-dev
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

COPY . .
#RUN apt-get install ffmpeg portaudio19-dev libavcodec-extra libasound2-dev

RUN poetry install

EXPOSE 8787

CMD poetry run gunicorn --bind :8787 -k uvicorn.workers.UvicornH11Worker --workers 4 app.main:app