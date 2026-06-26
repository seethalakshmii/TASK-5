from flask import Flask, request, jsonify
from database import get_connection
import boto3
import os

app = Flask(__name__)

# S3 Client
s3 = boto3.client("s3")

# Bucket name from environment variable
S3_BUCKET = os.environ.get("S3_BUCKET")


@app.route("/")
def home():
    return jsonify({"message": "Cloud Native DevOps Project"})


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


# -----------------------------
# Save data to RDS
# -----------------------------
@app.route("/submit", methods=["POST"])
def submit():

    try:

        data = request.get_json()

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
                data["message"],
            ),
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Saved to RDS successfully"})

    except Exception as e:

        return jsonify({"error": str(e)}), 500


# -----------------------------
# View database
# -----------------------------
@app.route("/users")
def users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)


# -----------------------------
# Upload file to S3
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload():

    try:

        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No filename"}), 400

        s3.upload_fileobj(
            file,
            S3_BUCKET,
            file.filename
        )

        return jsonify({
            "message": "File uploaded successfully to S3"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)