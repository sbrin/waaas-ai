# Dockerfile
FROM python:latest

WORKDIR /app

# Install Chromium and dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app
COPY ./app/main.py /app/main.py

# Expose port 8000
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
