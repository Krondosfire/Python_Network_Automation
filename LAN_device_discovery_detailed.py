# pip uninstall pyasn1
# pip install pyasn1==0.4.8


from scapy.all import ARP, Ether, srp
from pysnmp.hlapi import (SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, nextCmd)
import datetime
import os

def scan_network(network):
    """
    Scans the given network for active devices using ARP requests.
    Args:
        network (str): The network range to scan (e.g., '192.168.1.1/24').
    Returns:
        list: A list of dictionaries containing IP and MAC addresses of active devices.
    """
    devices = []
    try:
        # Create an ARP request packet
        arp_request = ARP(pdst=network)
        ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast MAC address
        packet = ether_frame / arp_request

        # Send the packet and receive responses
        answered, _ = srp(packet, timeout=2, verbose=False)

        # Parse responses to extract IP and MAC addresses
        for sent, received in answered:
            devices.append({"ip": received.psrc, "mac": received.hwsrc})

    except Exception as e:
        print(f"Error during network scan: {e}")

    return devices

def get_device_info(ip):
    """
    Attempts to retrieve device type and operating system using SNMP.
    Args:
        ip (str): The IP address of the device.
    Returns:
        dict: A dictionary containing the device type and operating system.
    """
    try:
        # Perform an SNMP query to fetch the sysDescr MIB (device description)
        iterator = nextCmd(
            SnmpEngine(),
            CommunityData('public', mpModel=0),  # Replace 'public' with your SNMP community string
            UdpTransportTarget((ip, 161), timeout=5, retries=2),
            ContextData(),
            ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'))  # sysDescr OID
        )

        for errorIndication, errorStatus, errorIndex, varBinds in iterator:
            if errorIndication or errorStatus:
                return {"type": "Unknown", "os": "Unknown"}

            for varBind in varBinds:
                sys_descr = str(varBind[1]).lower()
                if "cisco" in sys_descr:
                    return {"type": "Router", "os": "Cisco IOS"}
                elif "windows" in sys_descr:
                    return {"type": "PC", "os": "Windows"}
                elif "linux" in sys_descr or "ubuntu" in sys_descr:
                    return {"type": "Server", "os": "Linux"}
                elif "macos" in sys_descr or "darwin" in sys_descr:
                    return {"type": "PC", "os": "MacOS"}
                else:
                    return {"type": "Unknown", "os": sys_descr}

    except Exception as e:
        print(f"Error retrieving SNMP data from {ip}: {e}")
        return {"type": "Unknown", "os": "Unknown"}

def generate_report(devices):
    """
    Generates a report of discovered devices and saves it to a text file.
    Args:
        devices (list): List of dictionaries containing device information.
    """
    # Generate a unique filename with date and time stamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"network_devices_{timestamp}.txt"

    try:
        # Write device information to the file
        with open(filename, 'w') as file:
            file.write(f"Enhanced Network Device Discovery Report - {timestamp}\n")
            file.write("=" * 80 + "\n")
            file.write(f"{'IP Address':<20}{'MAC Address':<20}{'Device Type':<20}{'Operating System':<20}\n")
            file.write("-" * 80 + "\n")
            for device in devices:
                file.write(f"{device['ip']:<20}{device['mac']:<20}{device['type']:<20}{device['os']:<20}\n")

        print(f"Report generated successfully: {os.path.abspath(filename)}")

    except Exception as e:
        print(f"Error writing report: {e}")

if __name__ == "__main__":
    # Allow user input for network range
    network_range = input("Enter the network range to scan (e.g., '192.168.1.1/24'): ")
    
    print(f"Scanning network: {network_range}")
    discovered_devices = scan_network(network_range)

    if discovered_devices:
        print(f"Discovered {len(discovered_devices)} devices:")
        
        # Enrich data with device type and OS information
        for device in discovered_devices:
            info = get_device_info(device['ip'])
            device.update(info)
            print(f"IP: {device['ip']}, MAC: {device['mac']}, Type: {device['type']}, OS: {device['os']}")

        # Generate a report
        generate_report(discovered_devices)
    else:
        print("No devices found on the network.")
