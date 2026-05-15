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
def send_email():

    data = request.get_json()

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

        "html": f"""
        <h2>New Customer Request</h2>

        <p><b>Name:</b> {data['name']}</p>

        <p><b>Work:</b><br>{data['work']}</p>

        <p><b>Contact Method:</b> {data['contact_method']}</p>

        <p><b>Contact:</b> {data['contact']}</p>
        """
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    if response.status_code in [200, 202]:
        return jsonify({"success": True})

    return jsonify({
        "success": False,
        "error": response.text
    })


if __name__ == "__main__":
    app.run()
