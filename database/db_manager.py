# MOCK DATABASE MANAGER - PURE PYTHON NO DEPENDENCIES
import datetime

# --- REMOVED ALL FIREBASE IMPORTS ---

class MockDB:
    def collection(self, name):
        return MockCollection(name)

class MockCollection:
    def __init__(self, name):
        self.name = name

    def stream(self):
        # Return fake data for the dashboard
        if self.name == 'machines':
            return [
                MockDoc({'id': 'm1', 'name': 'CNC Lathe', 'status': 'Running', 'temperature': 65, 'vibration': 0.4}),
                MockDoc({'id': 'm2', 'name': 'Hydraulic Press', 'status': 'Idle', 'temperature': 24, 'vibration': 0.1}),
                MockDoc({'id': 'm3', 'name': 'Robotic Arm', 'status': 'Warning', 'temperature': 82, 'vibration': 1.2}),
                MockDoc({'id': 'm4', 'name': 'Conveyor Belt', 'status': 'Running', 'temperature': 45, 'vibration': 0.3})
            ]
        return []

    def document(self, doc_id):
        return MockDocumentReference(doc_id)
    
    def add(self, data):
        return None, None

class MockDoc:
    def __init__(self, data):
        self._data = data
        self.id = data.get('id', 'mock_id')
    
    def to_dict(self):
        return self._data

class MockDocumentReference:
    def __init__(self, doc_id):
        self.id = doc_id
    
    def set(self, data):
        pass

# GLOBAL FUNCTION TO GET DB
def init_firebase():
    print("✅ USING MOCK DATABASE (DEMO MODE)")
    return MockDB()
