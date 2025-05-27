FROM python:3.10-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the replicator code
COPY . .

# Run the replicator script
CMD ["python", "replicator.py"]
