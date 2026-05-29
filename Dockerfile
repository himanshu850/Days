FROM python:3.11-slim

WORKDIR /app

# Install build/runtime deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=5000
EXPOSE 5000

CMD ["python", "daysfrom.py"]
