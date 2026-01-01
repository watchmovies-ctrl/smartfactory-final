from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from config import Config
# We import get_db, but we DON'T import 'db' directly to avoid the NoneType error
from database.db_manager import init_firebase, get_db, get_all_machines, add_machine_to_db, delete_machine_from_db, toggle_machine_status, create_log_entry, get_settings_dict, update_settings_dict
from services.analytics_service import calculate_kpis, get_analytics_data
from werkzeug.security import check_password_hash
import random
from datetime import datetime
from firebase_admin import firestore

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Firebase on startup
with app.app_context():
    init_firebase()

# Middleware
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session: return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROUTES ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # FIX: Get DB connection only when needed
        db = get_db()
        
        # Query Firestore
        users_ref = db.collection('users').where('username', '==', username).limit(1).stream()
        user_doc = next(users_ref, None)
        
        if user_doc:
            user_data = user_doc.to_dict()
            if check_password_hash(user_data['password_hash'], password):
                session['user'] = username
                return redirect(url_for('dashboard'))
        
        return render_template('login.html', error="Invalid Cloud Credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', active_page='dashboard')

@app.route('/machines')
@login_required
def machines():
    m_list = get_all_machines()
    return render_template('machines.html', active_page='machines', machines=m_list)

@app.route('/machines/add', methods=['POST'])
@login_required
def add_machine():
    add_machine_to_db(request.form['name'], request.form['type'], request.form['capacity'])
    flash("Machine deployed to Cloud Database")
    return redirect(url_for('machines'))

@app.route('/machines/delete/<string:id>', methods=['POST'])
@login_required
def delete_machine(id):
    delete_machine_from_db(id)
    flash("Machine removed from Cloud")
    return redirect(url_for('machines'))

@app.route('/machines/toggle/<string:id>', methods=['POST'])
@login_required
def toggle_machine(id):
    toggle_machine_status(id)
    return redirect(url_for('machines'))

@app.route('/reports')
@login_required
def reports():
    db = get_db()
    docs = db.collection('production_logs').order_by('date', direction=firestore.Query.DESCENDING).limit(50).stream()
    logs = [doc.to_dict() for doc in docs]
    return render_template('reports.html', active_page='reports', logs=logs)

@app.route('/alerts')
@login_required
def alerts():
    db = get_db()
    docs = db.collection('alerts').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(20).stream()
    alerts_data = [doc.to_dict() for doc in docs]
    
    c = sum(1 for a in alerts_data if a.get('severity')=='Critical')
    w = sum(1 for a in alerts_data if a.get('severity')=='Warning')
    i = sum(1 for a in alerts_data if a.get('severity')=='Info')
    return render_template('alerts.html', active_page='alerts', alerts=alerts_data, c=c, w=w, i=i)

@app.route('/analytics')
@login_required
def analytics():
    data = get_analytics_data()
    return render_template('analytics.html', active_page='analytics', rankings=data['rankings'], trend_labels=data['trend']['labels'], trend_data=data['trend']['data'])

@app.route('/settings')
@login_required
def settings():
    s = get_settings_dict()
    return render_template('settings.html', active_page='settings', s=s)

@app.route('/settings/update', methods=['POST'])
@login_required
def update_settings():
    data = {
        'plant_name': request.form['plant_name'],
        'threshold_eff': float(request.form['threshold_eff']),
        'shift_hours': float(request.form['shift_hours'])
    }
    update_settings_dict(data)
    flash("Cloud Configuration Updated")
    return redirect(url_for('settings'))

@app.route('/api/dashboard')
@login_required
def api_data():
    return jsonify(calculate_kpis())

@app.route('/api/simulate')
@login_required
def simulate():
    db = get_db()
    today = db.collection('production_logs').where('date', '==', datetime.now().strftime('%Y-%m-%d')).stream()
    
    count = 0
    for doc in today:
        data = doc.to_dict()
        if data['actual_qty'] < data['planned_qty']:
            new_qty = data['actual_qty'] + random.randint(10, 50)
            new_run = data['runtime_hours'] + 0.5
            
            db.collection('production_logs').document(doc.id).update({
                'actual_qty': new_qty,
                'runtime_hours': round(new_run, 2)
            })
            count += 1
            
    if count == 0:
        machines = get_all_machines()
        for m in machines:
            if m.get('status') == 'Active':
                create_log_entry(m['id'], m['name'], int(m['capacity_per_hour']) * 8)
                
    return jsonify({"status": "Cloud Sync Complete"})

@app.route('/help')
@login_required
def help_page():
    return render_template('help.html', active_page='help')
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
