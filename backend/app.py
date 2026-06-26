from flask import Flask, request, jsonify
from database import get_connection
import boto3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

s3 = boto3.client("s3")

# ===========================
# Home
# ===========================
@app.route("/")
def home():
    return jsonify({"message": "Cloud Native DevOps Project"})


# ===========================
# Health
# ===========================
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


# ===========================
# Save form to RDS
# ===========================
@app.route("/submit", methods=["POST"])
def submit():
    try:
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
                data["message"],
            ),
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Saved to RDS"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===========================
# View users
# ===========================
@app.route("/users")
def users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)


# ===========================
# Upload file to S3
# ===========================
@app.route("/upload", methods=["POST"])
def upload():

    try:

        bucket = os.getenv("S3_BUCKET")

        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        filename = secure_filename(file.filename)

        s3.upload_fileobj(
            file,
            bucket,
            filename
        )

        return jsonify({
            "message": "Uploaded successfully!",
            "file": filename
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)