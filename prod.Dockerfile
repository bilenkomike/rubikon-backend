FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

FROM base AS builder
RUN apt-get update && apt-get install -y build-essential libpq-dev
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

FROM base
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*
COPY --from=builder /install /usr/local
COPY . .

RUN addgroup --system app && adduser --system --ingroup app app

RUN mkdir -p /app/staticfiles /app/media \
    && chown -R app:app /app

USER app

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
