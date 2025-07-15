from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime, timedelta
from twilio.rest import Client

app = Flask(__name__)
CORS(app)

# Initialize Twilio client
twilio_client = Client("YOUR_SID", "YOUR_SECRETCODE")
TWILIO_PHONE = "TWILIO_NO"  # Your Twilio phone number

# MongoDB connection
client = MongoClient("mongodb+srv://USER_NAME:PASSWORD@cluster0.ikhcjpi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["tyre_projects"]

def check_and_notify(phone, service_date):
    """Check if service date is 6+ months old and send notification"""
    six_months_ago = datetime.now() - timedelta(days=180)  # ~6 months
    
    if isinstance(service_date, str):
        service_date = datetime.strptime(service_date, "%Y-%m-%d")
    
    if service_date <= six_months_ago:
        try:
            message = twilio_client.messages.create(
                body=f"Reminder: Your last service was on {service_date.strftime('%Y-%m-%d')}. 🤯Now its time for a checkup! Inorder to keep your Car🚗 and you healthy😊",
                from_=TWILIO_PHONE,
                to=phone
            )
            return True
        except Exception as e:
            print(f"Twilio error: {e}")
            return False
    return False

@app.route('/save_date', methods=['POST'])
def save_date():
    try:
        # 1. Get and validate request data
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data received"}), 400
            
        service_date = data.get("service_date")
        if not service_date:
            return jsonify({"success": False, "error": "Service date is required"}), 400

        # 2. Get user session and phone number
        session_data = db.sessions.find_one()
        if not session_data or "email" not in session_data:
            return jsonify({"success": False, "error": "Session expired"}), 401
            
        user_data = db.users.find_one({"email": session_data["email"]})

# If user doesn't exist, create one with default phone number (or extract from session if available)
        if not user_data:
            default_phone = data.get("phone")  # Try to fetch phone from frontend if needed
            if not default_phone:
                return jsonify({"success": False, "error": "Phone number required to create user"}), 400
            db.users.insert_one({
                "email": session_data["email"],
                "phone_number": default_phone,
                "created_at": datetime.now()
            })
            phone = default_phone
        else:
            phone = user_data.get("phone")
            if not phone:
                return jsonify({"success": False, "error": "Phone number missing for existing user"}), 400


        # 3. Update or insert service date
        result = db.service_dates.update_one(
            {"phone_number": phone},
            {
                "$set": {
                    "service_date": service_date,
                    "last_updated": datetime.now()
                },
                "$setOnInsert": {
                    "created_at": datetime.now()
                }
            },
            upsert=True
        )

        # 4. Check if notification should be sent
        notification_sent = check_and_notify(phone, service_date)

        response = {
            "success": True,
            "message": "Service date saved successfully",
            "data": {
                "phone_number": phone,
                "service_date": service_date,
                "notification_sent": notification_sent
            }
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)