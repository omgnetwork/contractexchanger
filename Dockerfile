FROM python:alpine3.7

MAINTAINER Jake Bunce <jake@omise.co>

RUN apk add shadow curl

RUN groupadd --gid 1000 contractexchanger && \
    useradd \
      --uid 1000 \
      --gid 1000 \
      --create-home \
      --shell /bin/bash \
      contractexchanger

COPY . /home/contractexchanger/

WORKDIR /home/contractexchanger/

RUN pip3 install -r requirements.txt

USER contractexchanger

ENTRYPOINT ["./server.py"]
