from flask import Flask, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
import logging
from flask import render_template
from flask import send_from_directory
from flask import redirect


app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb+srv://USER_NAME:PASSWORD@cluster0.ikhcjpi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["tyre_projects"]
session_collection = db["sessions"]
users_collection = db['users']
@app.route("/logout", methods=["POST"])
def logout():
    try:
        session_collection.delete_many({})  # Remove all sessions
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/login")
def login_redirect():
    # Serve login.html directly from login folder
    return send_file("..//login//login.html")
@app.route("/delete_account", methods=["POST"])
def delete_account():
    try:
        print("Received delete request")

        # Step 1: Fetch the logged-in user's email from sessions
        session = session_collection.find_one()
        print("Session found:", session)  # Debug log

        if session and "email" in session:
            email = session["email"]
            print(f"User email from session: {email}")

            # Step 2: Delete user from 'users' collection
            delete_user_result = db["users"].delete_one({"email": email})
            if delete_user_result.deleted_count == 1:
                print(f"User {email} deleted successfully from users collection.")

                # Step 3: Delete associated records from 'services' collection
                delete_service_result = db["services"].delete_many({"email": email})
                print(f"Deleted {delete_service_result.deleted_count} services for user {email}.")

                # Step 4: Remove session
                session_collection.delete_one({"email": email})
                print(f"Session for {email} deleted successfully.")

                return jsonify({"message": "Account and services deleted successfully"}), 200
            else:
                print(f"No matching user found with email: {email}")
                return jsonify({"error": "No user found with this email"}), 404
        else:
            print("No email found in session")  # Debug log
            return jsonify({"error": "No user session found"}), 400
    except Exception as e:
        print("Error during account deletion:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/")
def user_details():
    # Get email from sessions collection (assuming there's only one session stored)
    session_data = session_collection.find_one()
    email = session_data.get('email') if session_data else None

    if email:
        # Find the user in users collection using the email
        user_data = users_collection.find_one({'email': email})

        if user_data:
            name = user_data.get('name', '')
            phone = user_data.get('phone', '')
            car_model = user_data.get('brand', '')
            car_brand = user_data.get('model', '')

            return render_template(
                'car.html',
                name=name,
                email=email,
                phone=phone,
                car_model=car_model,
                car_brand=car_brand
            )
    
    return "User not found or session missing", 404

@app.route('/')
def home():
    return render_template('car.html')  # This is in 'final/templates'

# Route for tyres/index.html (outside templates)
@app.route('/dashboard')
def tyres_dashboard():
    return redirect("http://172.16.52.187:5000/", code=302) # From 'tyres' folder

# Route for services/index.html (outside templates)
@app.route('/services')
def service_date():
    return send_from_directory('../services', 'index.html')  # From 'services' folder

# Route for Car_models/index.html (outside templates)
@app.route('/Car-models')
def car_model():
    return send_from_directory('../Car_models', 'index.html') 
if __name__ == "__main__":
    app.run(debug=True, port=5006)
