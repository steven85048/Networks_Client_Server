FROM python:alpine3.7
RUN mkdir -p /usr/src/server
WORKDIR /usr/src/server

ONBUILD COPY requirements.txt .
ONBUILD RUN pip3 install -r requirements.txt

ONBUILD COPY ./messaging_system .
EXPOSE 5006

CMD python3 -m messaging_system.server