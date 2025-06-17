
FROM python:3.11-slim


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        lilypond \
        wget \
        fonts-freefont-ttf \
        && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY src/ ./src
COPY main.py .

CMD ["python", "main.py"]
