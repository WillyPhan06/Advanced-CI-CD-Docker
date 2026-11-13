import os

from flask import Flask
import redis

app = Flask(__name__)

client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)

app_env = os.getenv("APP_ENV", "development")


@app.get("/")
def home():
    visits = client.incr("visits")

    return (
        f"Hello from Compose! "
        f"Environment: {app_env}. "
        f"Visits: {visits}\n"
    )


@app.get("/health")
def health():
    try:
        client.ping()
        return {"status": "healthy", "redis": "reachable"}, 200
    except redis.RedisError:
        return {
            "status": "unhealthy",
            "redis": "unreachable",
        }, 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)