FROM python:3.9-slim-buster


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      cmake \
      python3-dev \
      libopenblas-dev \
      libx11-6 \
      libgtk2.0-dev \
      pkg-config && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip config set global.timeout 1000 && \
    pip config set global.retries 5


RUN pip install --no-cache-dir -r requirements.txt


COPY fomm/ fomm/
COPY static/ static/
COPY models/ models/
COPY app/ app/
COPY s3_utils.py ./

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]