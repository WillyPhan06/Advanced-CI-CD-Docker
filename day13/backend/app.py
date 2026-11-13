from flask import Flask, jsonify, request
import psycopg
import os

brokenahh:
app = Flask(__name__)


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "tasksdb"),
        user=os.getenv("DB_USER", "taskuser"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health_check():
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")

        return {
            "status": "healthy",
            "database": "reachable"
        }, 200

    except psycopg.Error:
        return {
            "status": "unhealthy",
            "database": "unreachable"
        }, 503


# ==========================================
# GET ALL TASKS
# ==========================================

@app.get("/tasks")
def get_tasks():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, title, created_at
            FROM tasks
            ORDER BY id DESC
        """).fetchall()

    result = [
        {
            "id": row[0],
            "title": row[1],
            "created_at": row[2].isoformat()
        }
        for row in rows
    ]

    return jsonify(result)


# ==========================================
# CREATE A TASK
# ==========================================

@app.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title")

    # Validate task title
    if not isinstance(title, str) or not title.strip():
        return {"error": "Task title is required"}, 400

    # Insert task into database
    with get_connection() as conn:
        row = conn.execute("""
            INSERT INTO tasks (title)
            VALUES (%s)
            RETURNING id, title, created_at
        """, (title.strip(),)).fetchone()

    # Return created task
    return {
        "id": row[0],
        "title": row[1],
        "created_at": row[2].isoformat()
    }, 201


if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000)
