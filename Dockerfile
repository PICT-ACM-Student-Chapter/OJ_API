# FROM python:3-alpine
# ENV PYTHONUNBUFFERED 1

# RUN apk update

# RUN apk add --update --no-cache postgresql-client
# RUN apk add --update --no-cache --virtual .tmp-build-deps \
#       gcc libc-dev linux-headers postgresql-dev
# COPY ./app/requirements.txt /requirements.txt
# RUN pip install -r requirements.txt
# RUN apk del .tmp-build-deps

# RUN mkdir /app
# WORKDIR /app
# COPY ./app /app

# RUN adduser -D user
# RUN chmod -R 777 /app
# # USER user

FROM python:3.9-slim-bullseye as base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Create app directory
COPY ./app/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt 

# ---- Copy Files/Build ----
FROM base

WORKDIR /app

COPY ./app /app

RUN chmod -R 777 /app