import psutil
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def get_bandwidth_usage(interval=1):
    """
    Captures bandwidth usage statistics.
    Args:
        interval (int): Time interval in seconds for capturing data.
    Returns:
        tuple: Upload and download speeds in Mbps.
    """
    net_io_start = psutil.net_io_counters()
    time.sleep(interval)
    net_io_end = psutil.net_io_counters()

    upload_speed = (net_io_end.bytes_sent - net_io_start.bytes_sent) * 8 / interval / 1e6  # Mbps
    download_speed = (net_io_end.bytes_recv - net_io_start.bytes_recv) * 8 / interval / 1e6  # Mbps

    return upload_speed, download_speed

def update_graph(frame, upload_data, download_data, line_upload, line_download):
    """
    Updates the graph with current bandwidth usage data.
    Args:
        frame: Animation frame (not used directly).
        upload_data: List to store upload speed data.
        download_data: List to store download speed data.
        line_upload: Line object for upload speed.
        line_download: Line object for download speed.
    """
    upload_speed, download_speed = get_bandwidth_usage()

    # Append data and maintain a rolling window of the last 60 points
    upload_data.append(upload_speed)
    download_data.append(download_speed)
    
    if len(upload_data) > 60:
        upload_data.pop(0)
        download_data.pop(0)

    # Update line data
    line_upload.set_ydata(upload_data)
    line_download.set_ydata(download_data)
    
    # Update x-axis limits dynamically
    line_upload.set_xdata(range(len(upload_data)))
    line_download.set_xdata(range(len(download_data)))
    
    plt.gca().relim()
    plt.gca().autoscale_view()

def main():
    # Initialize plot
    fig, ax = plt.subplots()
    
    ax.set_title("Real-Time Bandwidth Usage")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Speed (Mbps)")
    
    line_upload, = ax.plot([], [], label="Upload Speed", color="orange")
    line_download, = ax.plot([], [], label="Download Speed", color="blue")
    
    ax.legend(loc="upper right")
    
    # Data storage for bandwidth usage
    upload_data = []
    download_data = []

    # Animation function
    ani = FuncAnimation(
        fig,
        update_graph,
        fargs=(upload_data, download_data, line_upload, line_download),
        interval=1000  # Update every second
    )

    plt.show()

if __name__ == "__main__":
    main()
