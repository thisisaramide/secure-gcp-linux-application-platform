import os

import psycopg
from psycopg.rows import dict_row
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "raitbyne_inventory")
DB_USER = os.environ.get("DB_USER", "inventory_app")
DB_PASSWORD = os.environ.get("DB_PASSWORD")


def get_connection():
    if not DB_PASSWORD:
        raise RuntimeError("DB_PASSWORD is not configured.")

    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        row_factory=dict_row,
    )


@app.get("/")
def index():
    return jsonify(
        application="Raitbyne Inventory",
        status="running",
        message="Inventory application API is online.",
    )


@app.get("/healthz")
def health_check():
    return jsonify(status="ok"), 200


@app.get("/api/items")
def list_items():
    with get_connection() as connection:
        items = connection.execute(
            """
            SELECT id, name, quantity, created_at
            FROM inventory_items
            ORDER BY id
            """
        ).fetchall()

    return jsonify(items)


@app.post("/api/items")
def create_item():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify(error="A JSON request body is required."), 400

    name = payload.get("name")
    quantity = payload.get("quantity")

    if not isinstance(name, str) or not name.strip():
        return jsonify(error="name must be a non-empty string."), 400

    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0:
        return jsonify(error="quantity must be a non-negative integer."), 400

    with get_connection() as connection:
        item = connection.execute(
            """
            INSERT INTO inventory_items (name, quantity)
            VALUES (%s, %s)
            RETURNING id, name, quantity, created_at
            """,
            (name.strip(), quantity),
        ).fetchone()

    return jsonify(item), 201


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
