FROM python:3

LABEL maintainer="tmunzer@juniper.net"
LABEL one.stag.mwts.version="1.0.0"
LABEL one.stag.mwts.release-date="2020-02-19"

COPY ./src /app/

WORKDIR /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir flask junos-eznc requests

EXPOSE 51361
CMD ["python","-u","/app/mwts.py"]

