FROM python:3

LABEL maintainer="tmunzer@juniper.net"
LABEL one.stag.mwtt.version="2.0.0"
LABEL one.stag.mwtt.release-date="2022-05-20"

RUN pip install --upgrade pip
RUN pip install --no-cache-dir flask requests

COPY ./src /app/
WORKDIR /app

RUN addgroup --gid 1000 -S mistlab && adduser --uid 1000 -S mistlab -G mistlab
RUN chown -R mistlab:mistlab /app
USER mistlab

EXPOSE 51361
CMD ["python","-u","/app/mwtt.py"]
