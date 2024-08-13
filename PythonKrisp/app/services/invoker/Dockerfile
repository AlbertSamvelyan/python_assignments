FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

ENV FLASK_APP=invoker.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]

