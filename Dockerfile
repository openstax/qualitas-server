FROM python:3.7-alpine

# Install base packages
RUN apk add --update --no-cache --virtual .build-deps gcc g++ postgresql-dev curl \
    libffi-dev tini yaml-dev python3-dev py3-psutil linux-headers musl-dev openssl-dev && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools && \
    rm -rf /var/cache/apk/*

# Install rustup for installing cryptography
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

WORKDIR /app

COPY ["requirements.txt", "/app"]

# Set cargo path so cryptography can install w/o errors
RUN source $HOME/.cargo/env && \
    pip install -r requirements.txt

COPY . .

# Set the application environment
ENV PYTHONIOENCODING utf_8
ENV PYTHONPATH /app:$PYTHONPATH
ENV PATH="/app/bin:${PATH}"
ENV FLASK_APP=/app/wsgi.py

# Heroku recommends running as a user but it didn't work
# FIXME: fix running docker container as user in dockerfile on Heroku
# Run as User
#RUN adduser -D myuser
#USER myuser

RUN chmod +x bin/docker-entrypoint.sh

CMD ["bin/docker-entrypoint.sh", "wsgi:app"]
