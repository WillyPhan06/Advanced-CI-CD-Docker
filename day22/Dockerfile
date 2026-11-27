FROM python:3.12-alpine

WORKDIR /app

ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}

COPY app.py .

EXPOSE 8000

CMD ["python", "app.py"]
