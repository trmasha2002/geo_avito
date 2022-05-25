FROM python:3

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /app
COPY requirements.txt ./
COPY app/users ./
RUN pip3 install -r requirements.txt

COPY . ./

RUN python3 runner.py
