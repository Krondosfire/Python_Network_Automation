from flask import Flask, render_template, request, redirect, url_for, flash
import time
import random
from threading import Thread

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Mock device data (replace with real device connections)
devices = [
    {"id": 1, "name": "Router-GJ3NFB", "ip_address": "192.168.1.1", "status": "up", "last_backup": None},
    {"id": 2, "name": "Switch-1", "status": "up", "last_backup": None},
    {"id": 3, "name": "Firewall-1", "status": "down", "last_backup": None}
]

def perform_backup(device):
    """Simulate backup process (replace with actual backup logic)"""
    try:
        # Simulate backup time
        time.sleep(random.uniform(1, 3))
        device["last_backup"] = time.strftime("%Y-%m-%d %H:%M:%S")
        return True
    except Exception as e:
        print(f"Backup failed: {str(e)}")
        return False

@app.route('/')
def dashboard():
    return render_template('dashboard.html', devices=devices)

@app.route('/backup', methods=['POST'])
def backup_devices():
    if request.method == 'POST':
        # Get selected device (for simplicity, we'll backup all devices)
        backup_thread = Thread(target=backup_all_devices)
        backup_thread.start()
        flash("Backup initiated for all devices...", "info")
    return redirect(url_for('dashboard'))

def backup_all_devices():
    """Backup all devices in background"""
    for device in devices:
        if perform_backup(device):
            print(f"Successfully backed up {device['name']}")
        else:
            print(f"Failed to backup {device['name']}")

if __name__ == '__main__':
    app.run(debug=True)
