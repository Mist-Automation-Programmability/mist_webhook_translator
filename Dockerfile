FROM python:3

LABEL maintainer="tmunzer@juniper.net"
LABEL one.stag.mwtt.version="1.1.0"
LABEL one.stag.mwtt.release-date="2020-04-08"


RUN pip install --upgrade pip
RUN pip install --no-cache-dir flask requests

COPY ./src /app/
WORKDIR /app

EXPOSE 51361
CMD ["python","-u","/app/mwtt.py"]

