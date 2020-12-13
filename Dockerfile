FROM python:3

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /app
COPY requirements.txt ./
COPY users ./
RUN pip3 install -r requirements.txt

COPY . ./

CMD uvicorn --host=0.0.0.0 main:app
