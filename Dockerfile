FROM python:3.10-slim


RUN mkdir /usr/src/http-zeversolar
WORKDIR /usr/src/http-zeversolar
ADD ./ .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]


