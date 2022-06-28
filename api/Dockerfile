FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app
RUN chmod +x /app/app/main.py

CMD cd /app && uvicorn app.main:app --host 0.0.0.0 --port 80