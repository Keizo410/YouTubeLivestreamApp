FROM python:3.8-slim-bullseye

WORKDIR /app

ENV PYTHONPATH=/app:$PYTHONPATH

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app

CMD ["gunicorn","--bind","0.0.0.0:8000", "--timeout","120", "server:app"]
