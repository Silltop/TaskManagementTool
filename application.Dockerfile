FROM debian:stable-slim

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* \
    && apt autoremove -y python3-pip \
    && rm requirements.txt

WORKDIR /app
COPY . /app/