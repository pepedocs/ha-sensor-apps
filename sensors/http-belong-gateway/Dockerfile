FROM python:3.10-slim

RUN apt update && apt install -y firefox-esr

RUN mkdir /usr/src/ha-sensor-apps
WORKDIR /usr/src/ha-sensor-apps
ADD ./ .

RUN pip install -r ./sensors/http-belong-gateway/requirements.txt

ENV PYTHONPATH=.

RUN chmod +x ./sensors/http-belong-gateway/geckodriver

ENTRYPOINT ["python", "./sensors/http-belong-gateway/app.py"]
