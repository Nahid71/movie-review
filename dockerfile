FROM python:3.9-slim

# create work directory
RUN mkdir -p /usr/src/app

# set work directory
WORKDIR /usr/src/app

# setup dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

# expose the given port
EXPOSE 8000

