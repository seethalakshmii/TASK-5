from flask import Flask, request, jsonify, Response
from database import get_connection
import boto3
import os
from werkzeug.utils import secure_filename

from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST
)

app = Flask(__name__)

s3 = boto3.client("s3")

# -------------------------------
# Prometheus Metrics
# -------------------------------

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Duration",
    ["endpoint"]
)


def record_metric(method, endpoint, status):
    REQUEST_COUNT.labels(method, endpoint, status).inc()


# -------------------------------
# Routes
# -------------------------------

@app.route("/")
def home():
    record_metric("GET", "/", "200")
    return jsonify({"message": "Cloud Native DevOps Project..Version 2"})


@app.route("/health")
def health():
    record_metric("GET", "/health", "200")
    return jsonify({"status": "healthy"})


@app.route("/submit", methods=["POST"])
def submit():
    timer = REQUEST_LATENCY.labels("/submit").time()

    try:
        with timer:
            data = request.json

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users(name,email,message)
                VALUES(%s,%s,%s)
                """,
                (
                    data["name"],
                    data["email"],
                    data["message"]
                )
            )

            conn.commit()

            cursor.close()
            conn.close()

            record_metric("POST", "/submit", "200")

            return jsonify({
                "message": "Saved to RDS"
            })

    except Exception as e:
        record_metric("POST", "/submit", "500")
        return jsonify({"error": str(e)}), 500


@app.route("/users")
def users():
    timer = REQUEST_LATENCY.labels("/users").time()

    with timer:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        record_metric("GET", "/users", "200")

        return jsonify(rows)


@app.route("/upload", methods=["POST"])
def upload():
    timer = REQUEST_LATENCY.labels("/upload").time()

    try:
        with timer:
            bucket = os.getenv("S3_BUCKET")

            if "file" not in request.files:
                record_metric("POST", "/upload", "400")
                return jsonify({"error": "No file uploaded"}), 400

            file = request.files["file"]

            if file.filename == "":
                record_metric("POST", "/upload", "400")
                return jsonify({"error": "No file selected"}), 400

            filename = secure_filename(file.filename)

            s3.upload_fileobj(file, bucket, filename)

            record_metric("POST", "/upload", "200")

            return jsonify({
                "message": "Uploaded successfully!",
                "file": filename
            })

    except Exception as e:
        record_metric("POST", "/upload", "500")
        return jsonify({"error": str(e)}), 500


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)