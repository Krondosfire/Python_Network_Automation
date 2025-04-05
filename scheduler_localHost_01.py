import schedule
import time
import subprocess

# Define functions to run each script
def run_extract_network_config():
    print("Running extract_networkConfig_localHost.py...")
    subprocess.run(["python", "extract_networkConfig_localHost.py"])

def run_get_sys_info():
    print("Running get_localHost_sysInfo.py...")
    subprocess.run(["python", "get_localHost_sysInfo.py"])

def run_active_app_and_traffic():
    print("Running activeApp_and_networkTraffic_localHost.py...")
    subprocess.run(["python", "activeApp_and_networkTraffic_localHost.py"])

# Schedule the scripts to run every 2 minutes
schedule.every(2).minutes.do(run_extract_network_config)
schedule.every(2).minutes.do(run_get_sys_info)
schedule.every(2).minutes.do(run_active_app_and_traffic)

print("Scheduler started. Scripts will run every 2 minutes.")

# Keep the scheduler running
while True:
    schedule.run_pending()
    time.sleep(1)
