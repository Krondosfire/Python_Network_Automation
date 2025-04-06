from scapy.all import sniff, IP, TCP, UDP, ICMP
import matplotlib.pyplot as plt
from collections import Counter
import datetime

def capture_traffic(interface=None, packet_count=100):
    """
    Captures network traffic and returns a list of packets.
    Args:
        interface (str): The network interface to capture traffic on (default: None for all interfaces).
        packet_count (int): The number of packets to capture.
    Returns:
        list: A list of captured packets.
    """
    print(f"Capturing {packet_count} packets on interface: {interface or 'all interfaces'}...")
    packets = sniff(iface=interface, count=packet_count, timeout=30)
    print(f"Captured {len(packets)} packets.")
    return packets

def analyze_traffic(packets):
    """
    Analyzes the captured packets and counts the occurrence of different protocols.
    Args:
        packets (list): A list of captured packets.
    Returns:
        dict: A dictionary with protocol names as keys and counts as values.
    """
    protocol_counts = Counter()

    for packet in packets:
        if IP in packet:
            if TCP in packet:
                protocol_counts["TCP"] += 1
            elif UDP in packet:
                protocol_counts["UDP"] += 1
            elif ICMP in packet:
                protocol_counts["ICMP"] += 1
            else:
                protocol_counts["Other"] += 1
        else:
            protocol_counts["Non-IP"] += 1

    return protocol_counts

def visualize_traffic(protocol_counts):
    """
    Visualizes the network traffic using a bar chart.
    Args:
        protocol_counts (dict): A dictionary with protocol names as keys and counts as values.
    """
    protocols = list(protocol_counts.keys())
    counts = list(protocol_counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(protocols, counts, color='skyblue')
    plt.xlabel("Protocol")
    plt.ylabel("Packet Count")
    plt.title("Network Traffic Visualization")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Save the graph with a timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"network_traffic_{timestamp}.png"
    
    plt.savefig(filename)
    print(f"Traffic visualization saved as {filename}")
    
    plt.show()

if __name__ == "__main__":
    # Set parameters for capturing traffic
    interface = None  # Set to your network interface (e.g., "eth0", "wlan0", "en0"), or leave None for all interfaces
    packet_count = 100

    # Capture network traffic
    packets = capture_traffic(interface=interface, packet_count=packet_count)

    # Analyze the captured traffic
    protocol_counts = analyze_traffic(packets)

    # Display analysis results
    print("\nProtocol Counts:")
    for protocol, count in protocol_counts.items():
        print(f"{protocol}: {count}")

    # Visualize the traffic data
    visualize_traffic(protocol_counts)
