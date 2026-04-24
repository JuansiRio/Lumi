FROM python:3.11-slim

WORKDIR /app

COPY apps/agents/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY apps/agents/ .

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
