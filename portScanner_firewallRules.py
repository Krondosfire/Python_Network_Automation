import socket
from contextlib import closing
import psutil
import datetime

def check_local_open_ports():
    """
    Checks and lists open TCP ports on the local machine.
    Returns:
        list: A list of open TCP ports.
    """
    connections = psutil.net_connections(kind='inet')
    listening_ports = [conn.laddr.port for conn in connections if conn.status == psutil.CONN_LISTEN]
    return sorted(set(listening_ports))  # Remove duplicates and sort

def scan_remote_ports(ip, port_range):
    """
    Scans a range of ports on a remote device to identify open ports.
    Args:
        ip (str): The IP address of the target device.
        port_range (tuple): A tuple specifying the range of ports to scan (start, end).
    Returns:
        list: A list of open ports on the remote device.
    """
    open_ports = []
    for port in range(port_range[0], port_range[1] + 1):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(1)  # Timeout for each connection attempt
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
    return open_ports

def save_to_file(local_ports, remote_ports, ip, port_range):
    """
    Saves the results to a text file with a timestamped filename.
    Args:
        local_ports (list): List of open local TCP ports.
        remote_ports (list): List of open remote TCP ports.
        ip (str): IP address of the remote device.
        port_range (tuple): Range of scanned remote ports.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"firewall_and_open_ports_{timestamp}.txt"
    
    with open(filename, 'w') as file:
        file.write(f"Firewall Rules and Open Ports Report - {timestamp}\n")
        file.write("=" * 50 + "\n\n")
        
        # Local Open Ports
        file.write("Local Open TCP Ports:\n")
        if local_ports:
            file.write(", ".join(map(str, local_ports)) + "\n\n")
        else:
            file.write("No open TCP ports found.\n\n")
        
        # Remote Open Ports
        file.write(f"Remote Open TCP Ports on {ip} (Range {port_range[0]}-{port_range[1]}):\n")
        if remote_ports:
            file.write(", ".join(map(str, remote_ports)) + "\n\n")
        else:
            file.write("No open TCP ports found.\n\n")

    print(f"[+] Results saved to {filename}")

if __name__ == "__main__":
    # Check local open ports
    print("[+] Checking local open TCP ports...")
    local_open_ports = check_local_open_ports()
    
    if local_open_ports:
        print(f"[+] Local Open TCP Ports: {local_open_ports}")
    else:
        print("[-] No open TCP ports found locally.")

    # Scan remote device for open ports
    ip = input("\nEnter the IP address of the remote device to scan: ")
    
    try:
        start_port = int(input("Enter start of port range to scan: "))
        end_port = int(input("Enter end of port range to scan: "))
        
        if start_port > end_port or start_port < 1 or end_port > 65535:
            raise ValueError("Invalid port range.")
        
        print(f"[+] Scanning remote device {ip} for open ports in range {start_port}-{end_port}...")
        remote_open_ports = scan_remote_ports(ip, (start_port, end_port))
        
        if remote_open_ports:
            print(f"[+] Remote Open TCP Ports: {remote_open_ports}")
        else:
            print("[-] No open TCP ports found on the remote device.")
        
        # Save results to file
        save_to_file(local_open_ports, remote_open_ports, ip, (start_port, end_port))
    
    except ValueError as e:
        print(f"[-] Error: {e}")
