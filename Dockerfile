FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        default-jre-headless \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

WORKDIR /app

# Copy source before editable install so the package resolves correctly
COPY pyproject.toml .
COPY src/ src/
RUN pip install --no-cache-dir -e ".[dev]"

COPY jobs/ jobs/

CMD ["bash"]
