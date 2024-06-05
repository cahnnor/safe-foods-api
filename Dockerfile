FROM python:3.10.14-alpine

COPY requirements.txt ./

RUN pip3 install -r requirements.txt
ENV FLASK_APP = main

WORKDIR /src
ENTRYPOINT flask --app /src/main.py --debug run --host 0.0.0.0