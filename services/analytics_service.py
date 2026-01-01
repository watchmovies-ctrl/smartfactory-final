from database.db_manager import get_db, get_logs_for_today, get_settings_dict

def calculate_kpis():
    logs = get_logs_for_today()
    settings = get_settings_dict()
    
    thresh = float(settings.get('threshold_eff', 75.0))
    shift_h = float(settings.get('shift_hours', 8.0))
    
    data = []
    total_eff, delays = 0, 0
    active_count = 0
    
    # In NoSQL, we iterate the list of dictionaries
    for log in logs:
        if not log.get('planned_qty'): continue
        
        active_count += 1
        eff = round((log['actual_qty'] / log['planned_qty'] * 100), 1)
        util = round((log['runtime_hours'] / shift_h * 100), 1)
        idle = round(shift_h - log['runtime_hours'], 1)
        
        status = "Good"
        if eff < thresh: status = "Critical"
        elif eff < (thresh + 15): status = "Warning"
        
        if log['actual_qty'] < log['planned_qty']: delays += 1
        
        data.append({
            "id": log['id'],
            "name": log.get('machine_name', 'Unknown'),
            "efficiency": eff,
            "utilization": util,
            "idle_time": idle,
            "actual_qty": log['actual_qty'],
            "planned_qty": log['planned_qty'],
            "status": status
        })
        total_eff += eff
        
    avg = round(total_eff / active_count, 1) if active_count > 0 else 0
    bottle = min(data, key=lambda x: x['efficiency'])['name'] if data else "None"
    
    return {
        "kpi_summary": {
            "avg_efficiency": avg, 
            "total_machines": len(data), 
            "delayed_orders": delays, 
            "bottleneck": bottle
        }, 
        "machines": data
    }

def get_analytics_data():
    # For a hackathon, we can just fetch all logs and aggregate in Python
    # Real production systems would use BigQuery or specialized counters
    db = get_db()
    logs = db.collection('production_logs').stream()
    
    # Aggregate by Machine
    machine_stats = {}
    
    for doc in logs:
        l = doc.to_dict()
        m_name = l.get('machine_name')
        if m_name not in machine_stats:
            machine_stats[m_name] = {'total_eff': 0, 'count': 0}
        
        if l['planned_qty'] > 0:
            eff = (l['actual_qty'] / l['planned_qty']) * 100
            machine_stats[m_name]['total_eff'] += eff
            machine_stats[m_name]['count'] += 1
            
    rankings = []
    for name, stats in machine_stats.items():
        avg = stats['total_eff'] / stats['count'] if stats['count'] else 0
        rankings.append({"name": name, "avg_eff": round(avg, 1)})
        
    rankings.sort(key=lambda x: x['avg_eff'], reverse=True)
    
    # Dummy trend for visual demo (aggregating dates in NoSQL is complex code)
    trend = {"labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "data": [65, 70, 68, 72, 75, 80, 78]}
    
    return {"rankings": rankings, "trend": trend}
