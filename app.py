from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.db_manager import init_firebase
import os

app = Flask(__name__)

# --- FIX 1: Hardcoded Secret Key to prevent Session Errors ---
app.secret_key = "hackathon-secret-key-123"

# Initialize DB (Mock or Real)
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

        # --- FIX 2: Hardcoded Login Check (Bypasses DB completely) ---
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

    # Fetch data from Mock DB safely
    machines = []
    try:
        # Check if db is valid before querying
        if db:
            machines_ref = db.collection('machines').stream()
            for doc in machines_ref:
                machines.append(doc.to_dict())
    except Exception as e:
        print(f"Error fetching data: {e}")

    # Calculate basic stats for the dashboard
    total_machines = len(machines)
    active_machines = sum(1 for m in machines if m.get('status') == 'Running')

    return render_template('dashboard.html', 
                         machines=machines, 
                         total_machines=total_machines,
                         active_machines=active_machines)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Vercel requires the app to be available as 'app'
if __name__ == '__main__':
    app.run(debug=True)
