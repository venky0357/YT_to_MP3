FROM python:3.11-slim

# Install required system packages including NodeJS & ffmpeg
RUN apt-get update && apt-get install -y \
    nodejs \
    ffmpeg \
    curl \
    && apt-get clean

# Install yt-dlp with EJS support and Python dependencies
RUN pip install --no-cache-dir yt-dlp[default] yt-dlp-ejs fastapi uvicorn

# Create app directory and copy app
WORKDIR /app
COPY . .

# Expose port for Render
EXPOSE 10000

# Start FastAPI/Uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
