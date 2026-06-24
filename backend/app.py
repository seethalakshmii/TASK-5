from flask import Flask, request, jsonify
from database import get_connection

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Cloud Native DevOps Project"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

# INSERT DATA TO RDS
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

    return jsonify({"message": "Saved to RDS"})

# GET DATA (VERIFY)
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