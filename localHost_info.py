import socket
import platform
import os

class LocalHostInfo:
    @staticmethod
    def get_hostname():
        """Retrieve the hostname of the local machine."""
        return socket.gethostname()

    @staticmethod
    def get_ip_address():
        """Retrieve the IP address of the local machine."""
        try:
            hostname = LocalHostInfo.get_hostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except socket.error:
            return "Unable to retrieve IP address"

    @staticmethod
    def get_os_info():
        """Retrieve operating system information."""
        os_name = platform.system()
        os_version = platform.version()
        os_release = platform.release()
        return f"{os_name} {os_release} (Version: {os_version})"

    @staticmethod
    def get_cpu_info():
        """Retrieve CPU information."""
        try:
            if platform.system() == "Windows":
                return platform.processor()
            elif platform.system() == "Linux":
                # Read CPU info from /proc/cpuinfo (Linux systems)
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "model name" in line:
                            return line.split(":")[1].strip()
            elif platform.system() == "Darwin":  # macOS
                return os.popen("sysctl -n machdep.cpu.brand_string").read().strip()
            else:
                return "CPU information not available"
        except Exception as e:
            return f"Error retrieving CPU info: {str(e)}"

    @staticmethod
    def collect_all_info():
        """Collect all local host parameters."""
        return {
            "Hostname": LocalHostInfo.get_hostname(),
            "IP Address": LocalHostInfo.get_ip_address(),
            "Operating System": LocalHostInfo.get_os_info(),
            "CPU Info": LocalHostInfo.get_cpu_info()
        }

# Main script execution
if __name__ == "__main__":
    print("Local Host Information:")
    info = LocalHostInfo.collect_all_info()
    for key, value in info.items():
        print(f"{key}: {value}")
