# Headless Chromium for real-browser runs and screenshots (ADR-0003).
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    SNACK_AND_LIFT_E2E=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends chromium chromium-driver fonts-liberation fonts-dejavu-core fonts-noto-color-emoji \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN python -m pip install --no-cache-dir --upgrade pip && python -m pip install --no-cache-dir -e ".[dev]"
COPY tests ./tests

RUN useradd --create-home --uid 1000 app \
    && mkdir -p /app/chrome_profile /app/screenshots \
    && chown -R app:app /app
USER app

ENTRYPOINT ["python", "-m", "snack_and_lift"]
