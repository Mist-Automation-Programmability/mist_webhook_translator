FROM python:3.13-slim
LABEL maintainer="tmunzer@juniper.net"
LABEL one.stag.wht.version="2.2.0"
LABEL one.stag.wht.release-date="2024-03-29"

RUN apt-get update && apt-get upgrade -y && apt-get install gcc libffi-dev -y

RUN python3 -m pip install --upgrade pip

COPY ./src /app/
WORKDIR /app

RUN python3 -m pip install -r requirements.txt

EXPOSE 51361
CMD ["python","-u","/app/app.py"]
