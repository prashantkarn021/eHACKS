import time
from datetime import datetime
from plyer import notification
import geocoder

def get_location():
    try:
        location = gps.get_location()
        if location:
            latitude = location.get("lat", "Unknown")
            longitude = location.get("lon", "Unknown")
            return f"Lat: {latitude}, Lon: {longitude}"
        else:
            return "Location not available"
    except Exception as e:
        return f"Error getting location: {e}"

def set_reminder():
    reminder_message = input("Enter your reminder message: ")
    reminder_time = input("Enter the reminder time (HH:MM 24-hour format): ")

    try:
        # Convert input time to a datetime object
        reminder_datetime = datetime.strptime(reminder_time, "%H:%M").time()

        print(f"Reminder set for {reminder_time}. Waiting...")

        while True:
            current_time = datetime.now().time()
            if current_time.hour == reminder_datetime.hour and current_time.minute == reminder_datetime.minute:
                notification.notify(
                    title="Reminder!",
                    message=reminder_message,
                    timeout=10  # Notification disappears after 10 seconds
                )
                print("Reminder alert! Check your notification.")
                break
            time.sleep(30)  # Check time every 30 seconds to reduce CPU usage

    except ValueError:
        print("Invalid time format. Please enter time in HH:MM format.")

# Run the reminder function
set_reminder()