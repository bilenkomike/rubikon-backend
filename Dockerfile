FROM python:3.11
WORKDIR /app
COPY . /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install -y python3-pip python3-cffi
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1
COPY entrypoint.sh /entrypoint
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]