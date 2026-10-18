# ---- build stage: itt települnek a függőségek ----
FROM python:3.13-slim AS builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Először csak a requirements.txt, így a függőség-réteg cache-elődik,
# és forráskód-változásnál nem töltődik le újra semmi.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- végső stage ----
FROM python:3.13-slim
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    DATA_DIR=/data

# Nem root user + írható adatmappa
RUN useradd --create-home --uid 1000 appuser \
    && mkdir /data && chown appuser:appuser /data

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY app.py .

USER appuser
VOLUME /data
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]