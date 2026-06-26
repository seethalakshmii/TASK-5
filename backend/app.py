from flask import Flask, request, jsonify
from database import get_connection
import os
import boto3

app = Flask(__name__)

ses = boto3.client("ses", region_name="us-west-1")

@app.route("/")
def home():
    return jsonify({"message": "Cloud Native DevOps Project"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


# INSERT + EMAIL
@app.route("/submit", methods=["POST"])
def submit():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, email, message) VALUES (%s, %s, %s)",
        (data["name"], data["email"], data["message"])
    )

    conn.commit()
    cursor.close()
    conn.close()

    sender_email = os.environ["SENDER_EMAIL"]
    receiver_email = os.environ["RECEIVER_EMAIL"]

    subject = "New Form Submission"

    body = f"""
New user submission received:

Name: {data['name']}
Email: {data['email']}
Message: {data['message']}
"""

    ses.send_email(
        Source=sender_email,
        Destination={
            "ToAddresses": [receiver_email]
        },
        Message={
            "Subject": {"Data": subject},
            "Body": {"Text": {"Data": body}}
        }
    )

    return jsonify({"message": "Saved to RDS + Email sent"})


@app.route("/users")
def users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)