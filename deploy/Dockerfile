FROM python:3.11-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install gunicorn

COPY . .
RUN chmod +x /usr/src/app/deploy/entrypoint.sh

ENTRYPOINT ["/usr/src/app/deploy/entrypoint.sh"]
