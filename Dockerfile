FROM python:3.11.10-alpine3.20

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY ./project /app
WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh",  "/entrypoint.sh" ]