FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN useradd --create-home --shell /usr/sbin/nologin appuser

USER appuser

EXPOSE 8080

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8080", "app:app"]
