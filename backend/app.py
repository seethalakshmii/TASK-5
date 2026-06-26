from flask import Flask, request, jsonify
from database import get_connection

app = Flask(__name__)

# -------------------------
# HEALTH CHECK
# -------------------------
@app.route("/")
def home():
    return jsonify({"message": "Cloud Native DevOps Project"}), 200


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


# -------------------------
# INSERT DATA TO RDS
# -------------------------
@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.json

        # Validate input
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return jsonify({"error": "Missing required fields"}), 400

        # DB connection
        conn = get_connection()
        cursor = conn.cursor()

        # Insert query
        cursor.execute(
            "INSERT INTO users (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Saved to RDS successfully"}), 200

    except Exception as e:
        # IMPORTANT: return real error for debugging
        return jsonify({"error": str(e)}), 500


# -------------------------
# FETCH USERS (DEBUG)
# -------------------------
@app.route("/users", methods=["GET"])
def users():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)