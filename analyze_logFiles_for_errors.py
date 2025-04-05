import re

def extract_critical_errors(log_file):
    with open(log_file, 'r') as file:
        for line in file:
            if re.search(r'critical', line.lower()):
                print(line.strip())

extract_critical_errors('system_logs.txt')

# A script that reads a log file and extracts lines containing the keyword "critical" using regular expressions.
# This can be useful for identifying critical errors in network device logs.