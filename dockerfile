FROM python:3.6.3
MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>
COPY requirements-docker.txt /requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /requirements.txt
RUN mkdir /static
RUN mkdir /src
WORKDIR /src
