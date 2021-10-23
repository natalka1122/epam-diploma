# syntax=docker/dockerfile:1
FROM python:3.8-alpine

WORKDIR /app

ARG SOURCE_DIR
COPY ${SOURCE_DIR}requirements.txt requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY ${SOURCE_DIR}. .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
