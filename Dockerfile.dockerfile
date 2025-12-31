# 1. Base Image: Use a lightweight Python version
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install system dependencies (needed for some python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements first (Caching strategy: only re-install if requirements change)
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application code
COPY src/ src/

# 7. Create a folder for the vector DB
RUN mkdir -p chroma_db_data

# 8. Set Python to not buffer logs (so we see them immediately)
ENV PYTHONUNBUFFERED=1

# 9. Default command (can be overridden)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]