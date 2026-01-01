import firebase_admin
from firebase_admin import credentials, firestore
from config import Config
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

# Global DB Client
db = None

def init_firebase():
    global db
    if not firebase_admin._apps:
        # Check if key exists
        if not os.path.exists(Config.FIREBASE_CREDENTIALS):
            print("❌ ERROR: serviceAccountKey.json not found!")
            print("👉 Please download it from Firebase Console -> Project Settings -> Service Accounts")
            return None
            
        cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase Connected Successfully!")
        seed_data_if_empty()
    return db

def get_db():
    if not db:
        return init_firebase()
    return db

def seed_data_if_empty():
    # Check if we have machines
    machines_ref = db.collection('machines')
    if not len(list(machines_ref.limit(1).stream())):
        print("⚡ Seeding Initial Data to Firestore...")
        
        # Add Users
        db.collection('users').add({
            'username': 'admin',
            'password_hash': generate_password_hash('admin123'),
            'role': 'admin'
        })
        
        # Add Machines
        machines = [
            {'name': 'CNC-01', 'type': 'Milling', 'capacity_per_hour': 100, 'status': 'Active'},
            {'name': 'PRESS-A', 'type': 'Press', 'capacity_per_hour': 500, 'status': 'Active'},
            {'name': 'PACK-01', 'type': 'Packing', 'capacity_per_hour': 1000, 'status': 'Active'}
        ]
        for m in machines:
            db.collection('machines').add(m)
            
        # Add Settings
        db.collection('settings').document('config').set({
            'plant_name': 'Nagpur Cloud Factory',
            'threshold_eff': 75.0,
            'shift_hours': 8.0
        })
        print("✅ Seeding Complete.")

# --- HELPER FUNCTIONS FOR APP.PY ---

def get_all_machines():
    docs = db.collection('machines').stream()
    # Convert to list of dicts with ID attached
    machines = []
    for doc in docs:
        m = doc.to_dict()
        m['id'] = doc.id
        machines.append(m)
    return machines

def add_machine_to_db(name, m_type, capacity):
    db.collection('machines').add({
        'name': name,
        'type': m_type,
        'capacity_per_hour': int(capacity),
        'status': 'Active'
    })

def delete_machine_from_db(doc_id):
    db.collection('machines').document(doc_id).delete()

def toggle_machine_status(doc_id):
    ref = db.collection('machines').document(doc_id)
    curr = ref.get().to_dict().get('status', 'Active')
    new_status = 'Maintenance' if curr == 'Active' else 'Active'
    ref.update({'status': new_status})

def get_logs_for_today():
    today = datetime.now().strftime('%Y-%m-%d')
    # Firestore filtering
    docs = db.collection('production_logs').where('date', '==', today).stream()
    return [dict(doc.to_dict(), id=doc.id) for doc in docs]

def create_log_entry(machine_id, machine_name, planned_qty):
    today = datetime.now().strftime('%Y-%m-%d')
    db.collection('production_logs').add({
        'machine_id': machine_id,
        'machine_name': machine_name, # Storing name denormalized for easier NoSQL access
        'date': today,
        'planned_qty': int(planned_qty),
        'actual_qty': 0,
        'runtime_hours': 0.0,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

def get_settings_dict():
    doc = db.collection('settings').document('config').get()
    if doc.exists:
        return doc.to_dict()
    return {'plant_name': 'Default Plant', 'threshold_eff': 75.0, 'shift_hours': 8.0}

def update_settings_dict(data):
    db.collection('settings').document('config').set(data, merge=True)
