FROM python:3.11-slim

WORKDIR /app

COPY . /app

ENV PYTHONPATH=/app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--bind=0.0.0.0:8000", "--workers=1", "--threads=2", "--worker-class=gthread", "app:app"]