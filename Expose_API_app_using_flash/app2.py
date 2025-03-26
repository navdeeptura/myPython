import re
import logging
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from sqlalchemy.engine import Engine
from sqlalchemy import event

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
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
}

def sanitize_output(data):
    """Sanitize sensitive data before displaying/logging"""
    for key, pattern in SENSITIVE_PATTERNS.items():
        data = pattern.sub(f"[REDACTED {key.upper()}]", data)
    return data

# Suspicious SQL Patterns for Security Monitoring
SUSPICIOUS_PATTERNS = [
    r"(--|\bDROP\b|\bDELETE\b|\bUPDATE\b|\bINSERT\b|\bSELECT\b.*\bFROM\b)",  # SQL injection
    r"(\bOR\b.*=.*\bOR\b|\bAND\b.*=.*\bAND\b)",  # Boolean-based injection
    r"1=1|admin|password|root",  # Common attack strings
    r"\bGRANT\b.*\bALL PRIVILEGES\b",  # Privilege escalation
]

def send_security_alert(query, source_ip):
    """Sends an email alert when suspicious activity is detected"""
    sender_email = "your_alert_email@example.com"
    receiver_email = "security_team@example.com"
    subject = "🚨 Security Alert: Suspicious Database Activity Detected"
    body = f"""
    Alert! Suspicious database activity detected.

    🔹 Query: {query}
    🔹 Source IP: {source_ip}

    Please investigate immediately.
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.starttls()
            server.login("your_alert_email@example.com", "your_password")
            server.sendmail(sender_email, receiver_email, msg.as_string())
            logging.info("[ALERT SENT] Suspicious query detected.")
    except Exception as e:
        logging.error(f"Failed to send alert email: {str(e)}")

# SQLAlchemy Event Listener to Monitor Database Queries
@event.listens_for(Engine, "before_cursor_execute")
def before_query_execute(conn, cursor, statement, parameters, context, executemany):
    """Logs and analyzes SQL queries for suspicious activity."""
    sanitized_query = statement.lower()
    source_ip = request.remote_addr if request else "Unknown"

    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, sanitized_query):
            logging.warning(f"[SUSPICIOUS QUERY] IP: {source_ip} - Query: {sanitized_query}")
            send_security_alert(sanitized_query, source_ip)
            break

    logging.info(f"[QUERY LOG] IP: {source_ip} - Query: {sanitized_query}")

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
        
        # Detect Android or iOS from User-Agent header
        user_agent = request.headers.get("User-Agent", "").lower()
        device_type = "Unknown"

        if "android" in user_agent:
            device_type = "Android"
        elif "iphone" in user_agent or "ios" in user_agent:
            device_type = "iOS"

        logging.info(f"Received Data from {device_type}: {data['data']}")

        # Sanitize the data before processing
        sanitized_data = sanitize_output(data["data"])
        logging.info(f"Received Data: {sanitized_data}")

        return jsonify({
            "message": "Data received",
            "sanitized": sanitized_data,
            "device_type": device_type
        }), 200

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
