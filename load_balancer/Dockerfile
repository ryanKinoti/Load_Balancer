FROM python:3.8-slim

WORKDIR /load_balancer

COPY . /load_balancer

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --upgrade "requests<2.29.0"

CMD ["python", "balancer.py"]