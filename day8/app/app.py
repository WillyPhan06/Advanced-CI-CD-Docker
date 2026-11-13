import os
from flask import Flask
import redis

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", "6379"))

client = redis.Redis(
    host=redis_host,
    port=redis_port,
    decode_responses=True,
)

@app.get("/")
def home():
    visits = client.incr("visits")
    return f"Hello from Compose! Visits: {visits}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)