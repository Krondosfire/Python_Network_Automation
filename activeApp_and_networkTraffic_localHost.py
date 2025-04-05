import psutil
import datetime
import os
from scapy.all import sniff, IP, TCP, UDP

def get_active_applications():
    """
    Fetches all active processes and their network connections.
    """
    active_apps = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Get network connections for the process
            connections = proc.connections(kind='inet')  # 'inet' filters for internet connections
            if connections:
                for conn in connections:
                    if conn.status == psutil.CONN_ESTABLISHED:
                        active_apps.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "local_address": f"{conn.laddr.ip}:{conn.laddr.port}",
                            "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                            "status": conn.status
                        })
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
    return active_apps

def capture_network_traffic(packet_list, packet):
    """
    Callback function to capture network packets.
    """
    if IP in packet:
        packet_info = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": packet[IP].src,
            "destination": packet[IP].dst,
            "protocol": packet[IP].proto,
            "size": len(packet)
        }
        packet_list.append(packet_info)

def monitor_system():
    """
    Monitors active applications and network traffic, and saves the data to a file.
    """
    # Generate a unique filename with date and time stamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"system_monitor_{timestamp}.txt"

    # Capture active applications
    active_apps = get_active_applications()

    # Capture network traffic for 10 seconds
    print("Capturing network traffic for 10 seconds...")
    captured_packets = []
    sniff(timeout=10, prn=lambda pkt: capture_network_traffic(captured_packets, pkt), store=False)

    # Save data to file
    with open(output_file, 'w') as file:
        file.write(f"System Monitor Report - {timestamp}\n")
        file.write("=" * 50 + "\n\n")
        
        # Write active applications
        file.write("Active Applications:\n")
        file.write("-" * 50 + "\n")
        for app in active_apps:
            file.write(f"PID: {app['pid']}, Name: {app['name']}, "
                       f"Local Address: {app['local_address']}, "
                       f"Remote Address: {app['remote_address']}, Status: {app['status']}\n")
        
        file.write("\n\n")

        # Write network traffic details
        file.write("Captured Network Traffic:\n")
        file.write("-" * 50 + "\n")
        for pkt in captured_packets:
            file.write(f"Timestamp: {pkt['timestamp']}, Source: {pkt['source']}, "
                       f"Destination: {pkt['destination']}, Protocol: {pkt['protocol']}, "
                       f"Size: {pkt['size']} bytes\n")

    print(f"System monitor report saved to: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    monitor_system()
