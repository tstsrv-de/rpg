FROM python:3.10-bullseye
ENV PYTHONUNBUFFERED 1
# check later 
# ENV PYTHONDONTWRITEBYTECODE 1
RUN /usr/local/bin/python -m pip install --upgrade pip
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
