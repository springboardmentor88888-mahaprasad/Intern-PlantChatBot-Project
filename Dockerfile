# ==============================================================================
# PlantDocBot — Production Dockerfile
# Builds the Streamlit frontend + FastAPI backend in a single container.
# Model is auto-downloaded from HuggingFace on first run.
# ==============================================================================

FROM python:3.11-slim

WORKDIR /app

# ---- System deps (ffmpeg for Whisper, curl for health checks) ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Python deps (cached layer — only re-runs when requirements.txt changes) ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Application code ----
COPY config/          ./config/
COPY backend/         ./backend/
COPY database/        ./database/
COPY frontend/        ./frontend/
COPY app.py           .
COPY packages.txt     .
COPY .env.example     .

# ---- Streamlit config ----
COPY .streamlit/      ./.streamlit/

# ---- Create dirs for runtime data ----
RUN mkdir -p models data

# ---- Environment ----
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true

# ---- Ports ----
EXPOSE 8501
EXPOSE 5000

# ---- Health check (Streamlit's built-in endpoint) ----
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# ---- Default: run Streamlit ----
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
