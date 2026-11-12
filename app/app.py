from flask import Flask, jsonify

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
