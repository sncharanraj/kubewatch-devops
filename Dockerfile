FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=kubewatch.settings

RUN useradd -m appuser
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles && chown -R appuser:appuser /app

# Collect static at build time (optional but recommended)
RUN python manage.py collectstatic --noinput

USER appuser

EXPOSE 8000

HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

CMD ["gunicorn", "kubewatch.wsgi:application", "--bind", "0.0.0.0:8000"]
