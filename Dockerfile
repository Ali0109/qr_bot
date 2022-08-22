FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /qr_bot
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
