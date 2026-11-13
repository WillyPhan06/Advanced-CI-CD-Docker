# Stage 1: Prepare application dependencies
FROM python:3.12-slim AS builder

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR /build

RUN python -m venv "${VIRTUAL_ENV}"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Production runtime
FROM python:3.12-slim AS runtime

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only the prepared Python environment
COPY --from=builder /opt/venv /opt/venv

# Copy the application
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]