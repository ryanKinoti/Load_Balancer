FROM python:3.8-slim

WORKDIR /server

COPY . /server

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "server.py"]
