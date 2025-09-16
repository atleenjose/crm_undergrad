import firebase_admin
from firebase_admin import credentials, db

# Service account JSON you downloaded
cred = credentials.Certificate("/Users/atleenjose/Projects/crm-dashboard/backend/crm-undergraduation-firebase-adminsdk-fbsvc-5df68007d8.json")

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://crm-undergraduation-default-rtdb.firebaseio.com/"
})
