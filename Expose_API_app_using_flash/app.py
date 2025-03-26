import re
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Setup Logging
logging.basicConfig(
    filename="db_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Regex patterns for sanitization
SENSITIVE_PATTERNS = {
    "email": re.compile(r"[\w\.-]+@[\w\.-]+\.\w+"),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    "canada_sin": re.compile(r"\b\d{3}-\d{3}-\d{3}\b"),  # Matches "123-456-789",
}

def sanitize_output(data):
    """Sanitize sensitive data before displaying/logging"""
    for key, pattern in SENSITIVE_PATTERNS.items():
        data = pattern.sub(f"[REDACTED {key.upper()}]", data)
    return data


# API Endpoint to Test from Android App
@app.route("/submit", methods=["POST"])
def submit_data():
    """Receives user data from the Android app"""
    try:

        # Check if request contains JSON
        if not request.is_json:
            return jsonify({"error": "Invalid JSON"}), 400

        # Parse JSON safely
        data = request.get_json()
        if "data" not in data:
            return jsonify({"error": "Missing 'data' field"}), 400
        
        user_agent = request.headers.get("User-Agent", "").lower()
        device_type = "Unknown"

        if "android" in user_agent:
            device_type = "Android"
        elif "iphone" in user_agent or "ios" in user_agent:
            device_type = "iOS"

        logging.info(f"Received Data from {device_type}: {data['data']}")

        sanitized_data = sanitize_output(data["data"])
        logging.info(f"Received Data: {sanitized_data}")
        return jsonify({"message": "Data received", "sanitized": sanitized_data}), 200

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
