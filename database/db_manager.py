# MOCK DATABASE MANAGER FOR HACKATHON DEMO
# This bypasses all Firebase connection errors
import datetime

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
        elif self.name == 'production_log':
            return [
                MockDoc({'timestamp': datetime.datetime.now(), 'product_id': 'P-101', 'quantity': 50, 'status': 'Completed'}),
                MockDoc({'timestamp': datetime.datetime.now(), 'product_id': 'P-102', 'quantity': 120, 'status': 'In Progress'})
            ]
        elif self.name == 'alerts':
            return [
                MockDoc({'severity': 'High', 'message': 'Overheating detected in Robotic Arm', 'timestamp': datetime.datetime.now()})
            ]
        return []

    def document(self, doc_id):
        return MockDocumentReference(doc_id)
    
    def add(self, data):
        print(f"Mock DB: Added {data} to {self.name}")
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
        print(f"Mock DB: Set data for {self.id}: {data}")

# GLOBAL FUNCTION TO GET DB
def init_firebase():
    print("✅ USING MOCK DATABASE (DEMO MODE)")
    return MockDB()
