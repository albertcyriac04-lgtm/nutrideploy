import firebase_admin
from firebase_admin import credentials, firestore, db
from django.conf import settings
import os

_firebase_app = None

def initialize_firebase():
    """Initializes Firebase Admin SDK using credentials from settings."""
    global _firebase_app
    if _firebase_app is not None:
        return _firebase_app

    cred_path = getattr(settings, 'FIREBASE_CREDENTIALS_PATH', None)
    db_url = getattr(settings, 'FIREBASE_DATABASE_URL', None)

    if not cred_path or not os.path.exists(cred_path):
        print("Firebase credentials path not found or invalid.")
        return None

    try:
        cred = credentials.Certificate(cred_path)
        options = {}
        if db_url:
            options['databaseURL'] = db_url
            
        _firebase_app = firebase_admin.initialize_app(cred, options)
        return _firebase_app
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return None

def get_firestore_client():
    """Returns a Firestore client instance."""
    app = initialize_firebase()
    if app:
        return firestore.client()
    return None

def get_realtime_db_reference(path='/'):
    """Returns a reference to the Realtime Database at the specified path."""
    app = initialize_firebase()
    if app:
        return db.reference(path)
    return None
