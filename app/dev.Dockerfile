# pull official base image
FROM python:3.10-alpine

# set work directory
WORKDIR /usr/src/panel

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk --no-cache add curl

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system  --dev

# copy project
COPY . .
