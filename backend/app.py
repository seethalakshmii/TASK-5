from flask import Flask, request, jsonify
from database import get_connection
import boto3
import os

app = Flask(__name__)

# -------------------------
# HEALTH CHECK
# -------------------------
@app.route("/api/")
def home():
    return jsonify({"message": "Cloud Native DevOps Project"}), 200


@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"}), 200


# -------------------------
# INSERT DATA TO RDS
# -------------------------
@app.route("/api/submit", methods=["POST"])
def submit():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "No input data"}), 400

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Saved to RDS"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------
# GET USERS (VERIFY DB)
# -------------------------
@app.route("/api/users", methods=["GET"])
def users():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "count": len(result),
            "data": result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------
# S3 UPLOAD TRIGGER (OPTIONAL API)
# -------------------------
@app.route("/api/upload", methods=["POST"])
def upload():
    try:
        s3 = boto3.client("s3")
        bucket = os.getenv("BUCKET_NAME")

        file = request.files["file"]

        s3.upload_fileobj(file, bucket, file.filename)

        return jsonify({"message": "Uploaded to S3"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)