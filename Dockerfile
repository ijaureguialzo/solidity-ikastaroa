FROM python:3.12

RUN apt update && apt install -y bash nano tini

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

ENTRYPOINT ["/usr/bin/tini", "--"]
