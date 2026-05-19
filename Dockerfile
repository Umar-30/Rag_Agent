# Use an official Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Copy the rest of the application code
COPY . .

# Create the uploads directory if it doesn't exist
RUN mkdir -p uploads

# Expose the ports for FastAPI (8000) and Streamlit (7860 - default for HF Spaces)
EXPOSE 8000
EXPOSE 7860

# Set Environment Variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Command to run both Backend and Frontend
# We use & to run FastAPI in the background and then start Streamlit
CMD ["sh", "-c", ".venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 & .venv/bin/streamlit run ui.py --server.port 7860 --server.address 0.0.0.0"]
