FROM python:3.8-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app

CMD ["python", "server.py"]