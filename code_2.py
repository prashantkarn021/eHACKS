from flask import Flask, request, jsonify
import googlemaps
import firebase_admin
from firebase_admin import credentials, db
import schedule
import time

# Initialize Firebase
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://your-database-url.firebaseio.com/"})

# Initialize Google Maps API
gmaps = googlemaps.Client(key="YOUR_GOOGLE_MAPS_API_KEY")

app = Flask(__name__)

# Store user locations
user_locations = {}

@app.route("/update_location", methods=["POST"])
def update_location():
    data = request.json
    user_id = data['user_id']
    latitude = data['latitude']
    longitude = data['longitude']

    # Store location in Firebase
    ref = db.reference(f'users/{user_id}/location')
    ref.set({'latitude': latitude, 'longitude': longitude})

    return jsonify({"message": "Location updated"}), 200

@app.route("/get_reminder", methods=["POST"])
def get_reminder():
    data = request.json
    user_id = data['user_id']
    location = data['location']  # E.g., "Gym"

    reminders = {
        "Gym": "Time to drink water!",
        "Home": "Take your medicine!",
    }

    return jsonify({"reminder": reminders.get(location, "No reminders")})

@app.route("/ping_family", methods=["POST"])
def ping_family():
    data = request.json
    user_id = data['user_id']
    message = data['message']

    # Fetch family members from Firebase
    family_ref = db.reference(f'users/{user_id}/family')
    family_members = family_ref.get()

    for member in family_members:
        print(f"Notifying {member} with message: {message}")

    return jsonify({"message": "Family members notified!"})

if __name__ == "__main__":
    app.run(debug=True)
    
def send_reminder():
    print("Reminder: Stay hydrated!")

schedule.every(30).minutes.do(send_reminder)

while True:
    schedule.run_pending()
    time.sleep(1)