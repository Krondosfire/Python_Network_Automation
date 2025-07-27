import os
import time
import random
import logging
from threading import Thread

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# Read secret key from environment variable for security
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'change_this_secret_in_production')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler()  # Logs to stderr by default
    ]
)

# Mock device data (ideally, stored in database or persistent storage)
devices = [
    {"id": 1, "name": "Router-GJ3NFB", "ip_address": "192.168.1.1", "status": "up", "last_backup": None},
    {"id": 2, "name": "Switch-1", "status": "up", "last_backup": None},
    {"id": 3, "name": "Firewall-1", "status": "down", "last_backup": None}
]


def perform_backup(device):
    """Simulate backup process (replace with actual backup logic)"""
    try:
        logging.info(f"Starting backup for device: {device['name']}")
        # Simulate backup time
        time.sleep(random.uniform(1, 3))
        device["last_backup"] = time.strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"Backup completed for device: {device['name']}")
        return True
    except Exception as e:
        logging.error(f"Backup failed for device {device['name']}: {str(e)}")
        return False


def backup_all_devices():
    """Backup all devices in background"""
    logging.info("Backup thread started")
    for device in devices:
        success = perform_backup(device)
        if success:
            logging.info(f"Successfully backed up {device['name']}")
        else:
            logging.error(f"Failed to backup {device['name']}")
    logging.info("Backup thread finished")


@app.route('/')
def dashboard():
    return render_template('dashboard.html', devices=devices)


@app.route('/backup', methods=['POST'])
def backup_devices():
    # Trigger backup in background thread to avoid blocking web request
    backup_thread = Thread(target=backup_all_devices, daemon=True)
    backup_thread.start()
    flash("Backup initiated for all devices...", "info")
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    # For production, do NOT use 'debug=True' or Flask's built-in server
    # Run this app with a production-grade WSGI server instead, example:
    # gunicorn -w 4 your_module:app
    app.run(host='0.0.0.0', port=5000, debug=False)
