from flask import Flask, request, jsonify
from database import get_connection
import boto3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

s3 = boto3.client("s3")

S3_BUCKET = os.getenv("S3_BUCKET")


# -------------------------------------------------
# HOME
# -------------------------------------------------

@app.route("/")
@app.route("/api/")
def home():
    return jsonify({
        "message": "Cloud Native DevOps Project"
    }), 200


# -------------------------------------------------
# HEALTH
# -------------------------------------------------

@app.route("/health")
@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


# -------------------------------------------------
# SAVE FORM TO RDS
# -------------------------------------------------

@app.route("/submit", methods=["POST"])
@app.route("/api/submit", methods=["POST"])
def submit():

    try:

        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return jsonify({"error": "Missing fields"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users(name,email,message)
            VALUES(%s,%s,%s)
            """,
            (name, email, message)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Saved to RDS successfully"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# -------------------------------------------------
# VIEW USERS
# -------------------------------------------------

@app.route("/users")
@app.route("/api/users")
def users():

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(rows)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# -------------------------------------------------
# FILE UPLOAD TO S3
# -------------------------------------------------

@app.route("/upload", methods=["POST"])
@app.route("/api/upload", methods=["POST"])
def upload():

    try:

        if "file" not in request.files:
            return jsonify({
                "error": "No file selected"
            }), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({
                "error": "Empty filename"
            }), 400

        filename = secure_filename(file.filename)

        s3.upload_fileobj(
            file,
            S3_BUCKET,
            filename
        )

        return jsonify({
            "message": f"{filename} uploaded successfully"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# -------------------------------------------------
# RUN
# -------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )