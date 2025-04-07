import psutil
import time
import socket
import argparse
from datetime import datetime

def get_bandwidth_stats(interval=1, previous_io=None):
    """Get network bandwidth statistics"""
    current_io = psutil.net_io_counters()
    if previous_io:
        upload = (current_io.bytes_sent - previous_io.bytes_sent) * 8 / interval / 1e6  # Mbps
        download = (current_io.bytes_recv - previous_io.bytes_recv) * 8 / interval / 1e6  # Mbps
        return upload, download, current_io
    return 0, 0, current_io

def measure_latency(host="8.8.8.8", port=53, timeout=1):
    """Measure network latency using TCP connection time"""
    try:
        start = time.time()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
        return (time.time() - start) * 1000  # Convert to milliseconds
    except (socket.error, socket.timeout):
        return None

def main(log_file=None):
    previous_io = None
    print("Starting network monitor... (Ctrl+C to stop)")
    
    try:
        while True:
            start_time = time.time()
            
            # Get bandwidth stats
            upload, download, previous_io = get_bandwidth_stats(
                interval=1, previous_io=previous_io
            )
            
            # Measure latency
            latency = measure_latency()
            
            # Prepare output
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            output = (
                f"{timestamp} | "
                f"Upload: {upload:.2f} Mbps | "
                f"Download: {download:.2f} Mbps | "
                f"Latency: {latency:.1f} ms" if latency else "Latency: N/A"
            )
            
            # Update console display
            print(output, end='\r', flush=True)
            
            # Log to file if specified
            if log_file:
                with open(log_file, "a") as f:
                    f.write(output + "\n")
            
            # Sleep to maintain interval
            time.sleep(max(0, 1 - (time.time() - start_time)))
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-time Network Monitor")
    parser.add_argument("--log", help="Log file path for saving statistics")
    args = parser.parse_args()
    
    main(log_file=args.log)
