# Dockerfile for PlantDocBot
# TODO: Replace placeholder comments with your actual implementation

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# TODO: Add system dependencies if needed (e.g., ffmpeg, build tools)
# Example:
# RUN apt-get update && apt-get install -y \
#     ffmpeg \
#     && rm -rf /var/lib/apt/lists/*

# TODO: Copy requirements first for better caching
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# TODO: Copy application code
# COPY app.py .
# COPY backend/ ./backend/
# COPY knowledge/ ./knowledge/
# COPY database/ ./database/
# COPY .streamlit/ ./.streamlit/

# TODO: Copy model files (if not using volume mount)
# COPY models/ ./models/

# TODO: Create necessary directories
# RUN mkdir -p data uploads

# TODO: Set environment variables
# ENV PYTHONPATH=/app
# ENV STREAMLIT_SERVER_PORT=8501
# ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# TODO: Expose Streamlit port
# EXPOSE 8501

# TODO: Add health check
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD curl -f http://localhost:8501/_stcore/health || exit 1

# TODO: Run the application
# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# NOTE: This is a template Dockerfile.
# Uncomment the sections above and customize for your needs.
# Make sure to update the COPY commands based on your actual project structure.
