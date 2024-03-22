FROM python:3.13.0a4-slim

LABEL maintainer="tmunzer@juniper.net"
LABEL one.stag.wht.version="2.0.0"
LABEL one.stag.wht.release-date="2022-05-20"

RUN apt-get update && apt-get upgrade -y && apt-get install gcc libffi-dev -y

RUN pip install --upgrade pip
RUN pip install --no-cache-dir flask requests

COPY ./src /app/
WORKDIR /app

RUN python3 -m pip install -r requirements.txt

EXPOSE 51361
CMD ["python","-u","/app/app.py"]
