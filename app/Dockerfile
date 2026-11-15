FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --create-home \
    --shell /usr/sbin/nologin appuser

USER 10001:10001

EXPOSE 8080

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8080", "app:app"]
