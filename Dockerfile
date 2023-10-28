FROM python:3.10
ENV PYTHONUNBUFFERED 1

WORKDIR /fastapi_app

COPY . .
RUN apt-get update && apt-get install -y postgresql-client
RUN apt-get install -y libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1
RUN pip install --upgrade pip && pip install -r requirements.txt


RUN chmod +x docker/run.sh
RUN chmod +x docker/tmp.sh
RUN chmod +x src/parser/parser.py