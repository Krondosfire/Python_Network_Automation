import socket
import platform
import os
import subprocess
import psutil
from datetime import datetime

class SystemInfoCollector:
    @staticmethod
    def get_host_info():
        """Get hostname and IP configuration"""
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return {
                "Hostname": hostname,
                "IP Address": ip_address,
                "All IPs": [addr.address for addr in psutil.net_if_addrs().values()]
            }
        except Exception as e:
            return {"Error": str(e)}

    @staticmethod
    def get_os_info():
        """Get operating system information"""
        return {
            "System": platform.system(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine()
        }

    @staticmethod
    def get_cpu_info():
        """Get CPU information"""
        try:
            if platform.system() == "Windows":
                return platform.processor()
            elif platform.system() == "Linux":
                with open("/proc/cpuinfo", "r") as f:
                    lines = [line.strip() for line in f if "model name" in line]
                return lines[0].split(":")[1] if lines else "Unknown"
            elif platform.system() == "Darwin":
                return subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
            return "Unknown"
        except Exception as e:
            return f"Error: {str(e)}"

    @staticmethod
    def get_memory_info():
        """Get memory information"""
        mem = psutil.virtual_memory()
        return {
            "Total": f"{mem.total / (1024**3):.2f} GB",
            "Available": f"{mem.available / (1024**3):.2f} GB",
            "Used Percent": f"{mem.percent}%"
        }

    @staticmethod
    def get_disk_info():
        """Get storage device information"""
        disks = []
        for part in psutil.disk_partitions():
            usage = psutil.disk_usage(part.mountpoint)
            disks.append({
                "Device": part.device,
                "Mount": part.mountpoint,
                "Total": f"{usage.total / (1024**3):.2f} GB",
                "Used": f"{usage.used / (1024**3):.2f} GB",
                "Free": f"{usage.free / (1024**3):.2f} GB"
            })
        return disks

    @staticmethod
    def get_processes():
        """Get running processes"""
        return [proc.info for proc in psutil.process_iter(['pid', 'name', 'username'])]

    @staticmethod
    def get_open_ports():
        """Get open network ports"""
        ports = []
        for conn in psutil.net_connections():
            if conn.status == 'LISTEN':
                ports.append(f"{conn.laddr.ip}:{conn.laddr.port}")
        return list(set(ports))

    @staticmethod
    def collect_all():
        """Collect all system information"""
        return {
            "System Information": {
                "Host Info": SystemInfoCollector.get_host_info(),
                "OS Info": SystemInfoCollector.get_os_info(),
                "CPU Info": SystemInfoCollector.get_cpu_info(),
                "Memory": SystemInfoCollector.get_memory_info(),
                "Storage": SystemInfoCollector.get_disk_info(),
                "Processes": SystemInfoCollector.get_processes()[:10],  # Top 10
                "Open Ports": SystemInfoCollector.get_open_ports()
            },
            "Timestamp": datetime.now().isoformat()
        }

    @staticmethod
    def save_to_file(filename="LocalHost_report.txt"):
        """Save system information to a text file"""
        data = SystemInfoCollector.collect_all()
        
        with open(filename, "w") as f:
            f.write("SYSTEM INFORMATION REPORT\n")
            f.write("=" * 40 + "\n\n")
            
            # Host Information
            f.write("[HOST INFORMATION]\n")
            for key, value in data['System Information']['Host Info'].items():
                f.write(f"{key}: {value}\n")
            
            # OS Information
            f.write("\n[OPERATING SYSTEM]\n")
            for key, value in data['System Information']['OS Info'].items():
                f.write(f"{key}: {value}\n")
            
            # Hardware Information
            f.write("\n[HARDWARE INFORMATION]\n")
            f.write(f"CPU: {data['System Information']['CPU Info']}\n")
            for key, value in data['System Information']['Memory'].items():
                f.write(f"Memory {key}: {value}\n")
            
            # Storage Information
            f.write("\n[STORAGE DEVICES]\n")
            for disk in data['System Information']['Storage']:
                f.write(f"\nDevice: {disk['Device']}\n")
                f.write(f"Mount: {disk['Mount']}\n")
                f.write(f"Total: {disk['Total']}\n")
                f.write(f"Used: {disk['Used']}\n")
                f.write(f"Free: {disk['Free']}\n")
            
            # Network Information
            f.write("\n[NETWORK PORTS]\n")
            for port in data['System Information']['Open Ports']:
                f.write(f"- {port}\n")
            
            # Processes
            f.write("\n[RUNNING PROCESSES (First 10)]\n")
            for proc in data['System Information']['Processes']:
                f.write(f"PID {proc['pid']}: {proc['name']} ({proc['username']})\n")
            
            f.write(f"\nReport generated at: {data['Timestamp']}\n")

if __name__ == "__main__":
    SystemInfoCollector.save_to_file()
    print("System report generated successfully!")
