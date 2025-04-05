
def extract_critical_errors(log_file):
    with open(log_file, 'r') as file:
        for line in file:
            if 'critical' in line.lower():
                print(line.strip())

# Example usage
extract_critical_errors('system_logs.txt')
