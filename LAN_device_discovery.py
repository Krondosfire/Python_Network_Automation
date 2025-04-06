from scapy.all import ARP, Ether, srp
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
            file.write(f"Network Device Discovery Report - {timestamp}\n")
            file.write("=" * 50 + "\n")
            file.write(f"{'IP Address':<20}{'MAC Address':<20}\n")
            file.write("-" * 50 + "\n")
            for device in devices:
                file.write(f"{device['ip']:<20}{device['mac']:<20}\n")

        print(f"Report generated successfully: {os.path.abspath(filename)}")

    except Exception as e:
        print(f"Error writing report: {e}")

if __name__ == "__main__":
    # Define the network range to scan (adjust based on your LAN subnet)
    network_range = "192.168.1.1/24"

    print(f"Scanning network: {network_range}")
    discovered_devices = scan_network(network_range)

    if discovered_devices:
        print(f"Discovered {len(discovered_devices)} devices:")
        for device in discovered_devices:
            print(f"IP: {device['ip']}, MAC: {device['mac']}")

        # Generate a report
        generate_report(discovered_devices)
    else:
        print("No devices found on the network.")
