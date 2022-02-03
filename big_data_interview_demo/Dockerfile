FROM python:3.7.12
LABEL maintainer rex.ultra
ENV PYTHONUNBUFFERED 1
RUN mkdir /project
RUN mkdir /project/log
RUN apt-get -y update

WORKDIR /project
COPY . /project
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod a+x docker-entrypoint.sh
RUN apt-get -y install vim

ENTRYPOINT ["./docker-entrypoint.sh"]
