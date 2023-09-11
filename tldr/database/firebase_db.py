import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("config/credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def validate_preferences(preferences: dict) -> bool:
    """Simple validation for user preferences."""
    # Assuming two settings for demonstration purposes
    valid_themes = ['light', 'dark']
    valid_notifications = ['on', 'off']
    
    theme = preferences.get('theme')
    notifications = preferences.get('notifications')
    
    if theme not in valid_themes:
        return False
    if notifications not in valid_notifications:
        return False
    
    return True

def fetch_user_preferences(user_id: str) -> dict:
    """Fetch user preferences from Firebase based on user ID."""
    try:
        user_ref = db.collection('users').document(user_id)
        return user_ref.get().to_dict()
    except Exception as e:
        print(f"Error fetching user preferences: {e}")
        return None

def save_user_preferences(user_id: str, preferences: dict):
    """Save user preferences to Firebase."""
    try:
        if not validate_preferences(preferences):
            print("Invalid preferences provided.")
            return
        
        user_ref = db.collection('users').document(user_id)
        user_ref.set(preferences)
    except Exception as e:
        print(f"Error saving user preferences: {e}")

def update_user_preferences(user_id: str, updated_prefs: dict):
    """Update specific user preferences in Firebase."""
    try:
        if not validate_preferences(updated_prefs):
            print("Invalid preferences provided.")
            return
        
        current_prefs = fetch_user_preferences(user_id)
        
        # Check if preferences are actually different
        if current_prefs == updated_prefs:
            print("Preferences are the same, no update required.")
            return
        
        user_ref = db.collection('users').document(user_id)
        user_ref.update(updated_prefs)
    except Exception as e:
        print(f"Error updating user preferences: {e}")

# ... (any other required Firebase operations)
