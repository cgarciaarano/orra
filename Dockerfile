# Set the base image to Ubuntu
FROM python:3.5-alpine

MAINTAINER cgarciaarano@gmail.com

# Update the repository sources list
RUN apk update

WORKDIR /opt/app

# Install Python packages and system build dependencies
# RUN apk add g++ make libffi-dev && \
# 	pip install -r requirements.txt && \
# 	apk del g++ make libffi-dev && \
# 	rm -rf /var/cache/apk/*

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy code
COPY *.py /opt/app/

ENTRYPOINT ["/usr/local/bin/python", "parser.py"]