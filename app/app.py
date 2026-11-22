import os

import psycopg
from flask import Flask, jsonify, request
from psycopg.rows import dict_row

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "raitbyne_inventory")
DB_USER = os.environ.get("DB_USER", "inventory_app")


def get_secret_value(name):
    secret_file = os.environ.get(f"{name}_FILE")

    if secret_file:
        try:
            with open(secret_file, encoding="utf-8") as file:
                return file.read().strip()
        except OSError as error:
            raise RuntimeError(
                f"Unable to read the secret file configured by {name}_FILE."
            ) from error

    return os.environ.get(name)


def get_connection():
    db_password = get_secret_value("DB_PASSWORD")

    if not db_password:
        raise RuntimeError("Database password is not configured.")

    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=db_password,
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
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, quantity, created_at
                FROM inventory_items
                ORDER BY id;
                """
            )
            items = cursor.fetchall()

    return jsonify(items), 200


@app.post("/api/items")
def create_item():
    payload = request.get_json(silent=True) or {}

    name = payload.get("name")
    quantity = payload.get("quantity")

    if not isinstance(name, str) or not name.strip():
        return jsonify(error="name must be a non-empty string"), 400

    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0:
        return jsonify(error="quantity must be a non-negative integer"), 400

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO inventory_items (name, quantity)
                VALUES (%s, %s)
                RETURNING id, name, quantity, created_at;
                """,
                (name.strip(), quantity),
            )
            item = cursor.fetchone()
        connection.commit()

    return jsonify(item), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
