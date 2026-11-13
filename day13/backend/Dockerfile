# Build stage
FROM python:3.12-slim AS builder

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR /build

RUN python -m venv "${VIRTUAL_ENV}"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# Runtime stage
FROM python:3.12-slim AS runtime

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd --system app && \
    useradd --system --gid app \
    --home-dir /app --no-create-home app

COPY --from=builder --chown=app:app /opt/venv /opt/venv
COPY --chown=app:app app.py .

USER app

EXPOSE 5000

CMD ["python", "app.py"]