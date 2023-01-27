FROM python:3.10-slim

RUN mkdir /usr/src/ha-sensor-apps
WORKDIR /usr/src/ha-sensor-apps
ADD ./ .
RUN pip install -r ./sensors/http-zeversolar/requirements.txt

ENV PYTHONPATH=.

ENTRYPOINT ["python", "./sensors/http-zeversolar/app.py"]


