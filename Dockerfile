FROM python:3.10.14-alpine3.20

COPY requirements.txt /temp/
COPY . /src
WORKDIR /src

RUN sh -c "pip -r install temp/requirements.txt"

