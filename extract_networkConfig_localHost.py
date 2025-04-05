import os
import subprocess
import datetime


def extract_network_configuration():
    # Get the current working directory
    current_dir = os.getcwd()
    
    # Generate a unique filename with date and time stamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(current_dir, f"network_config_{timestamp}.txt")


    try:
        # Execute the command to get network configuration (platform-dependent)
        if subprocess.os.name == "nt":    # Windows OS
            command = ["ipconfig", "/all"]
        else:  # Unix/Linux OS
            command = ["ifconfig", "-a"]

        # Run the command and capture the output

        result = subprocess.run(command, stdout=subprocess.PIPE,
stderr=subprocess.PIPE, text=True)
            
        # Check if the command executed successfully
        if result.returncode == 0:
            # Write the output to the file
            with open(output_file, 'w') as file:
                file.write(result.stdout)
            print(f"Network configuration has been saved to: {output_file}")
        else:
            print(f"Error executing command: {result.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Run the function
extract_network_configuration()  # Call the function to extract network configuration

