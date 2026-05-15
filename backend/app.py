from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("MAILERSEND_API_KEY")

@app.route("/")

def home():
    return "MP Auto Mechanics backend running"

@app.route("/send-email", methods=["POST"])

@app.route("/test")
def test():
    return {
        "api_key_exists": API_KEY is not None,
        "api_key_length": len(API_KEY) if API_KEY else 0
    }

@app.route("/send-email", methods=["POST"])
def send_email():

    try:
        data = request.json

        print("Received:", data)

        name = data.get("name")
        work = data.get("work")
        contact_method = data.get("contact_method")
        contact = data.get("contact")

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

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if response.status_code in [200, 202]:
            return jsonify({
                "success": True
            })

        return jsonify({
            "success": False,
            "error": response.text
        }), 500

    except Exception as e:
        print("ERROR:", str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run()
