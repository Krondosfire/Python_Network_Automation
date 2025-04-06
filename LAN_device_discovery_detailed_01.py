import os
import datetime

def get_device_info_via_snmp(ip, community="public"):
    """
    Fetch device information using SNMP command-line tools.
    Args:
        ip (str): IP address of the device.
        community (str): SNMP community string (default: 'public').
    Returns:
        dict: A dictionary containing device type and operating system.
    """
    try:
        # Execute snmpget command to fetch sysDescr
        command = f"snmpget -v2c -c {community} {ip} 1.3.6.1.2.1.1.1.0"
        result = os.popen(command).read()

        if "Cisco" in result:
            return {"type": "Router", "os": "Cisco IOS"}
        elif "Windows" in result:
            return {"type": "PC", "os": "Windows"}
        elif "Linux" in result or "Ubuntu" in result:
            return {"type": "Server", "os": "Linux"}
        elif "MacOS" in result or "Darwin" in result:
            return {"type": "PC", "os": "MacOS"}
        else:
            return {"type": "Unknown", "os": result.strip()}

    except Exception as e:
        print(f"Error retrieving SNMP data from {ip}: {e}")
        return {"type": "Unknown", "os": "Unknown"}

def generate_report(devices):
    """
    Generates a report of discovered devices and saves it to a text file.
    Args:
        devices (list): List of dictionaries containing device information.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"network_devices_{timestamp}.txt"

    try:
        with open(filename, 'w') as file:
            file.write(f"Enhanced Network Device Discovery Report - {timestamp}\n")
            file.write("=" * 80 + "\n")
            file.write(f"{'IP Address':<20}{'Device Type':<20}{'Operating System':<20}\n")
            file.write("-" * 80 + "\n")
            for device in devices:
                file.write(f"{device['ip']:<20}{device['type']:<20}{device['os']:<20}\n")

        print(f"Report generated successfully: {filename}")

    except Exception as e:
        print(f"Error writing report: {e}")

if __name__ == "__main__":
    # Define IPs to scan (replace with actual IPs)
    ip_addresses = ["192.168.1.1", "192.168.1.100", "192.168.1.101"]
    
    devices = []
    for ip in ip_addresses:
        info = get_device_info_via_snmp(ip)
        devices.append({"ip": ip, **info})

    generate_report(devices)
