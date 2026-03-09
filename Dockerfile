FROM python:3.10-slim

WORKDIR /app

# Install build dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose Dashboard Port
EXPOSE 5000

# Volume for SQLite persistence
VOLUME ["/app/storage"]

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Start both the job engine (scheduler) and the dashboard
CMD ["sh", "-c", "python main.py & python dashboard/app.py"]
