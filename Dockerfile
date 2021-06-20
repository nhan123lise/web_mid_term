FROM selenium/node-firefox:4.0.0-rc-1-prerelease-20210618
LABEL authors=SeleniumHQ

USER 1200


RUN sudo apt-get update -y
RUN sudo apt-get install -y python3-pip python-dev build-essential

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1

ENV APP_HOME /usr/src/app
WORKDIR /$APP_HOME

COPY . $APP_HOME/
