FROM python:3.12-slim

WORKDIR /app

ENV \
	PYTHONPATH="/app"

RUN \
    apt-get update && apt-get install -y \
    build-essential \
    curl \
    libcurl4-openssl-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install flask curl-cffi m3u8 gunicorn

COPY --link proxy.so sitecustomize.py ./

EXPOSE 7860

CMD ["gunicorn", "--workers", "5", "--worker-class", "gthread", "--threads", "4", "--bind", "0.0.0.0:7860", "proxy:app"]
