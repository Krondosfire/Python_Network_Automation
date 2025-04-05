import re
import datetime

def extract_critical_errors(input_log_file):
    # Generate a unique log file name based on date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_log_file = f"critical_errors_{timestamp}.txt"

    # Open the input log file and create a new output log file
    with open(input_log_file, 'r') as infile, open(output_log_file, 'w') as outfile:
        for line in infile:
            if re.search(r'critical', line.lower()):  # Search for "critical" in each line
                outfile.write(line.strip() + '\n')  # Write the critical error to the new log file

    print(f"Critical errors have been extracted to: {output_log_file}")

# Example usage
extract_critical_errors('system_logs.txt')
# A script that reads a log file, extracts lines containing the keyword "critical", and writes them to a new log file with a timestamp in the filename. This is useful for archiving critical errors separately.
# This can be useful for identifying critical errors in network device logs
# and archiving them for future reference. The output log file is named with a timestamp to avoid overwriting previous logs.
# This script can be run periodically to keep track of critical errors in network devices. It can also be integrated into a larger network monitoring system.