from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
# import googlemaps
import schedule
import time
from geopy.distance import geodesic

# Initialize Firebase
cred = credentials.Certificate("F:/ehacks2/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

# Initialize Google Maps API
# gmaps = googlemaps.Client(key="YOUR_GOOGLE_MAPS_API_KEY")

app = Flask(__name__)

# Function: Calculate Distance
def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km  # Distance in KM

# Store a Location-Based Reminder
@app.route("/set_reminder", methods=["POST"])
def set_reminder():
    data = request.json
    user_id = data.get('user_id')
    location_name = data.get('location_name')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    reminder_text = data.get('reminder_text')

    if not all([user_id, location_name, latitude, longitude, reminder_text]):
        return jsonify({"error": "Missing parameters"}), 400

    # Store reminder in Firebase
    ref = db.reference(f'users/{user_id}/reminders')
    ref.push({
        "location_name": location_name,
        "latitude": latitude,
        "longitude": longitude,
        "reminder_text": reminder_text
    })

    return jsonify({"message": "Reminder set successfully!"}), 200

# Update User Location
@app.route("/update_location", methods=["POST"])
def update_location():
    data = request.json
    user_id = data.get('user_id')
    latitude = float(data.get('latitude'))
    longitude = float(data.get('longitude'))

    if not user_id or not latitude or not longitude:
        return jsonify({"error": "Missing parameters"}), 400

    # Store location in Firebase
    db.reference(f'users/{user_id}/location').set({
        'latitude': latitude,
        'longitude': longitude
    })

    return jsonify({"message": "Location updated!"})

# Background Task to Check Reminders Every 5 Minutes
def check_reminders():
    users_ref = db.reference("users")
    users = users_ref.get()

    if not users:
        return

    for user_id, user_data in users.items():
        if "location" not in user_data or "reminders" not in user_data:
            continue

        user_location = user_data["location"]
        reminders = user_data["reminders"]

        latitude = float(user_location["latitude"])
        longitude = float(user_location["longitude"])

        triggered_reminders = []

        # Check if user is near any saved reminder location
        for reminder in reminders.values():
            reminder_lat = float(reminder["latitude"])
            reminder_lng = float(reminder["longitude"])

            distance = calculate_distance(latitude, longitude, reminder_lat, reminder_lng)

            if distance < 0.05:  # 50 meters threshold
                triggered_reminders.append(reminder["reminder_text"])

        # Send triggered reminders
        if triggered_reminders:
            print(f"🔔 Sending reminders to {user_id}: {triggered_reminders}")

# Schedule Reminder Checks Every 5 Minutes
schedule.every(5).minutes.do(check_reminders)

# Run the Scheduler in a Background Thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

import threading
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

if __name__ == "__main__":
    app.run(debug=True)