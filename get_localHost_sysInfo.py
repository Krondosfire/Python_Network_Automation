import psutil
import datetime
import os
import subprocess
import platform

def get_system_metrics():
    try:
        # Get timestamp for filename
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"system_status_{timestamp}.txt"
        
        # Get CPU usage percentage
        cpu_load = psutil.cpu_percent(interval=1)
        
        # Get memory usage
        memory = psutil.virtual_memory()
        memory_load = memory.percent
        
        # Get running services (platform-specific)
        running_services = []
        system_os = platform.system()
        
        if system_os == "Windows":
            for service in psutil.win_service_iter():
                if service.status() == 'running':
                    running_services.append(service.name())
        elif system_os == "Linux":
            try:
                services = subprocess.check_output(
                    ['systemctl', 'list-units', '--type=service', '--state=running'],
                    text=True
                )
                running_services = [line.split()[0] for line in services.split('\n') if '.service' in line]
            except subprocess.CalledProcessError:
                running_services = ["Unable to retrieve services - requires root privileges"]
        
        # Create report content
        report = f"""System Status Report - {timestamp}
========================================

CPU Load: {cpu_load}%
Memory Usage: {memory_load}%

Running Services:
----------------
"""
        report += '\n'.join(running_services) if running_services else "No services information available"

        # Save to file
        with open(filename, 'w') as f:
            f.write(report)
            
        print(f"System status report saved to: {os.path.abspath(filename)}")
        
    except ImportError:
        print("Error: psutil module not installed. Install with 'pip install psutil'")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    get_system_metrics()
