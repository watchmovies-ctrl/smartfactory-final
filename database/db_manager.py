import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import base64

# ... (rest of imports)

def init_firebase():
    global db
    if not firebase_admin._apps:
        # Check for Environment Variable
        cred_env = os.environ.get('FIREBASE_CREDENTIALS')
        
        if cred_env:
            # TRY TO DECODE BASE64 (The Fix)
            try:
                decoded_json = base64.b64decode(cred_env).decode('utf-8')
                cred_dict = json.loads(decoded_json)
            except:
                # Fallback: Maybe it wasn't base64, just regular JSON
                cred_dict = json.loads(cred_env)
                
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
        elif os.path.exists("serviceAccountKey.json"):
            # Local fallback
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            
    return db
