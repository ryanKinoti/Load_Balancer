FROM python:3.8-slim

WORKDIR /load_balancer

COPY . /load_balancer

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "load_balancer.py"]