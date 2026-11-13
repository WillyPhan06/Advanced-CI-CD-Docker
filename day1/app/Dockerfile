FROM python:3.10-slim-bookworm

WORKDIR /app

ENV APP_NAME="SWARM-DAY-2"

RUN echo "This happens during image build"

COPY app_2.py .

COPY app.py .

RUN pip install python-dotenv

ENTRYPOINT ["python"]