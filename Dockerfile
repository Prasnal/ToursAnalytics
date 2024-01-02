FROM python:3.12.1-alpine3.19

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.7


RUN apk add --update \
  build-base \
  gcc \
  python3-dev \
  rust \
  cargo \
  libffi-dev \
  openssl-dev \
  py-pip \
  zlib-dev \
  jpeg-dev \
  postgresql-dev


COPY requirements.txt /tmp/requirements.txt
#RUN pip install --user -r /tmp/requirements.txt
RUN pip install requests
RUN pip install beautifulsoup4
COPY ./ /opt/scraper
WORKDIR /opt/scraper

CMD python main.py
