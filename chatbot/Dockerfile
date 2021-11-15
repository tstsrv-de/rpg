#Tells Docker to use the official python 3 image from dockerhub as a base image
FROM python:3
# Sets an environmental variable that ensures output from python is sent straight to the terminal without buffering it first
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# Sets the container's working directory to /app
WORKDIR /app
# Copies all files from our local project into the container
COPY . /app
# runs the pip install command for all packages listed in the requirements.txt file
ONBUILD RUN apt-get update && apt-get upgrade -y
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install install tensorflow 
RUN pip install install numpy 
RUN pip install install nltk 
RUN pip install install tflearn 

