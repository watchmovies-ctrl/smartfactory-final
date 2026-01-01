from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.db_manager import init_firebase
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random key

# Initialize Firebase
db = init_firebase()

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple Admin Check
        if username == "admin" and password == "admin123":
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    machines = []
    try:
        # REAL FIREBASE FETCH
        if db:
            machines_ref = db.collection('machines').stream()
            for doc in machines_ref:
                machines.append(doc.to_dict())
    except Exception as e:
        print(f"Error fetching data: {e}")

    return render_template('dashboard.html', machines=machines)

if __name__ == '__main__':
    app.run(debug=True)
