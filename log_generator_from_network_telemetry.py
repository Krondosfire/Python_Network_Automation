
# ✅ Define function first
def log_telemetry(data):
    import logging
    # Configure logger (example)
    logging.basicConfig(
        filename='network_logs.txt',
        level=logging.INFO,
        format='%(asctime)s - %(message)s'
    )
    for entry in data:
        logging.info(f"Data: {entry}")

# Now call the function
telemetry_data = ["Latency: 50ms", "Throughput: 1Gbps"]
log_telemetry(telemetry_data)
