import firebase_admin
from firebase_admin import credentials, firestore

# Path to your downloaded firebase-adminsdk.json
cred = credentials.Certificate("F:/ehacks2/firebase-adminsdk.json")  # Replace with the path to your file
firebase_admin.initialize_app(cred)
print("Firebase initialized!")

# Access Firestore database
db = firestore.client()

doc_ref = db.collection('reminders').document('test_reminder')

# Set data in the document
doc_ref.set({
    'title': 'Test Reminder',
    'description': 'This is a test reminder',
    'completed': False
})

print("Test document added!")