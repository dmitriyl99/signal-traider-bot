FROM python:3.10-slim

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN chmod +x /app/app/main.py

CMD cd /app && python -m app.main