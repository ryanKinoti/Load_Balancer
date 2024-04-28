FROM python:3.8-slim

WORKDIR /server

COPY . /server

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "server.py"]
