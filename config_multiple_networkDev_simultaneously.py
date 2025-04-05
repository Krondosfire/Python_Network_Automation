from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor

# Define the device details
devices = [
    {"device_type": "cisco_ios", "host": "10.0.0.1", "username": "admin", "password": "password"},
    {"device_type": "cisco_ios", "host": "10.0.0.2", "username": "admin", "password": "password"},
]

# Define the command to be executed on each device

def configure_device(device):
    connection = ConnectHandler(**device)
    connection.send_config_set(["interface GigabitEthernet0/1", "description Configured by script"])
    connection.disconnect()

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(configure_device, devices)  # Execute the function for each device in parallel

    # A script that reads device IPs and credentials from a file, establishes SSH connections using Netmiko, 
    # and pushes configuration commands in parallel using multithreading to save time."