from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("MAILERSEND_API_KEY")


# =========================================
# HOME ROUTE
# =========================================
@app.route("/")
def home():
    return "MP Auto Mechanics backend running"


# =========================================
# TEST ROUTE
# =========================================
@app.route("/test")
def test():
    return {
        "api_key_exists": API_KEY is not None,
        "api_key_length": len(API_KEY) if API_KEY else 0
    }


# =========================================
# SEND EMAIL FUNCTION
# =========================================
def send_email(name, work, contact_method, contact):

    url = "https://api.mailersend.com/v1/email"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "from": {
            "email": "info@mpautomechanics.com",
            "name": "MP Auto Mechanics"
        },

        "to": [
            {
                "email": "mpautoelectrics@gmail.com",
                "name": "Admin"
            }
        ],

        "subject": "New Customer Request",

        "text": f"""
Customer Name: {name}
Work Details: {work}
Contact Method: {contact_method}
Contact Info: {contact}
""",

        "html": f"""
<h2>New Customer Request</h2>

<p><b>Name:</b> {name}</p>

<p><b>Work:</b> {work}</p>

<p><b>Contact Method:</b> {contact_method}</p>

<p><b>Contact Info:</b> {contact}</p>
"""
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    print("MAILERSEND STATUS:", response.status_code)
    print("MAILERSEND RESPONSE:", response.text)

    if response.status_code in [200, 202]:
        return True

    return False


# =========================================
# SEND EMAIL ROUTE
# =========================================
@app.route("/send-email", methods=["POST"])
def send_email_route():

    try:

        data = request.get_json()

        print("RECEIVED DATA:", data)

        success = send_email(
            data["name"],
            data["work"],
            data["contact_method"],
            data["contact"]
        )

        if success:

            return jsonify({
                "success": True
            })

        else:

            return jsonify({
                "success": False
            }), 500

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================================
# RUN APP
# =========================================
if __name__ == "__main__":
    app.run()
