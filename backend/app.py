from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("MAILERSEND_API_KEY")

@app.route("/send-email", methods=["POST"])
def send_email():

    try:
        data = request.get_json()

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

Work:
{work}

Contact Method:
{contact_method}

Contact:
{contact}
""",

            "html": f"""
<h2>New Customer Request</h2>

<p><b>Name:</b> {name}</p>

<p><b>Work:</b><br>{work}</p>

<p><b>Contact Method:</b> {contact_method}</p>

<p><b>Contact:</b> {contact}</p>
"""
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )

        print(response.text)

        if response.status_code in [200, 202]:
            return jsonify({
                "success": True
            })

        return jsonify({
            "success": False,
            "error": response.text
        }), 500

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
