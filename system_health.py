"""
System Health Check Script
Description: Generates a system health report including CPU, memory, disk usage, uptime,
network connectivity, response time, and Windows services.
Outputs both to terminal (with colors) and a timestamped log file.
"""

import psutil
import platform
import datetime
import socket
import os
import re
import time

# Get current date and time
now = datetime.datetime.now()

# Create a Logs folder if it doesn't exist
if not os.path.exists("Logs"):
    os.makedirs("Logs")

# Create a log file inside Logs folder with timestamp
log_filename = f"Logs/system_health_{now.strftime('%d-%m-%Y_%H-%M-%S')}.txt"
log_file = open(log_filename, "w")

# Function to print to terminal and log to file (strips ANSI color codes for file)
def log_print(message):
    print(message)               # Print to terminal with colors

    # Remove ANSI color for file
    clean_message = re.sub(r'\033\[[0-9;]*m', '', message)
    log_file.write(clean_message + "\n") 

# ------------------ HEADER ------------------
log_print("=" * 45)
log_print("          SYSTEM HEALTH CHECK REPORT       ")
log_print("=" * 45)
log_print(f"Report generated on: {now.strftime('%d-%m-%Y %H:%M:%S')}\n")

# ------------------ SYSTEM INFO ------------------
os_name = platform.system()         
os_version = platform.release()     
computer_name = platform.node()     
os_details = platform.platform()
os_architecture = platform.architecture()[0]

# Print and log system info
log_print(f"Computer Name: {computer_name}")
log_print(f"Operating System: {os_name} {os_version}")
log_print(f"System Details: {os_details} ({os_architecture})")

# ------------------ SYSTEM UPTIME ------------------
boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
uptime_seconds = (datetime.datetime.now() - boot_time).total_seconds()
days = int(uptime_seconds // 86400)
hours = int((uptime_seconds % 86400) // 3600)
minutes = int ((uptime_seconds % 3600) // 60)
log_print(f"System Uptime: {days} days, {hours} hours, {minutes} minutes\n")

# ------------------ CPU INFO ------------------
cpu_usage = psutil.cpu_percent(interval=1)
cpu_cores = psutil.cpu_count()
cpu_freq = psutil.cpu_freq()

# CPU usage with color warning
if cpu_usage > 80:
    log_print(f"CPU Usage: \033[91m{cpu_usage}% [HIGH CPU]\033[0m")
else:
    log_print(f"CPU Usage: \033[92m{cpu_usage}%\033[0m")

# CPU hardware details
if cpu_freq:
    log_print(f"CPU Hardware: {cpu_cores} cores @ {cpu_freq.current/1000:.1f}GHz")
else:
    log_print(f"CPU Hardware: {cpu_cores} cores (frequency info not available)")

# ------------------ MEMORY INFO ------------------
memory = psutil.virtual_memory()
total_gb = memory.total / (1024**3)
used_gb = memory.used / (1024**3)

# Memory usage with warning if high
if memory.percent > 80:
    log_print(f"Memory Usage: \033[91m{used_gb:.1f}GB used / {total_gb:.1f}GB total ({memory.percent}%) [HIGH MEMORY]\033[0m")
else:
    log_print(f"Memory Usage: \033[92m{used_gb:.1f}GB used / {total_gb:.1f}GB total ({memory.percent}%)\033[0m")

# ------------------ DISK INFO ------------------
partitions = psutil.disk_partitions()

for partition in partitions:
    try:
        disk = psutil.disk_usage(partition.mountpoint)

        # Calculate GB values for disk                     
        total_gb = disk.total / (1024**3)
        used_gb = disk.used / (1024**3)
        free_gb = disk.free / (1024**3)
        
        # Disk usage with color warnings                    
        if disk.percent > 90:
            log_print(f"{partition.device} Usage: \033[91m{used_gb:.1f}GB used / {total_gb:.1f}GB total ({free_gb:.1f}GB free) ({disk.percent}%) [LOW DISK SPACE]\033[0m")
        elif disk.percent > 75:
            log_print(f"{partition.device} Usage: \033[93m{used_gb:.1f}GB used / {total_gb:.1f}GB total ({free_gb:.1f}GB free) ({disk.percent}%) [DISK CAUTION]\033[0m")
        else:
            log_print(f"{partition.device} Usage: \033[92m{used_gb:.1f}GB used / {total_gb:.1f}GB total ({free_gb:.1f}GB free) ({disk.percent}%)\033[0m")
            
    except Exception as e:
        log_print(f"{partition.device}: \033[91mCould not read disk ({e})\033[0m")

# ------------------ NETWORK CONNECTIVITY ------------------
test_sites = [
    ("8.8.8.8", 53, "Google DNS"),
    ("1.1.1.1", 53, "Cloudflare DNS"),
    ("google.com", 80, "Google Web"),
]

log_print("\n--- NETWORK CONNECTIVITY ---")
successful_connections = 0
total_tests = len(test_sites)

for hostname, port, description in test_sites:
    try:
        sock = socket.create_connection((hostname, port), timeout=3)
        log_print(f"{description}: \033[92mConnected to {hostname}:{port}\033[0m")
        sock.close()
        successful_connections += 1
    except Exception as e:
        log_print(f"{description}: \033[91mFailed to connect to {hostname}:{port} ({e})\033[0m")
        

# Network summary
if successful_connections == total_tests:
    log_print(f"Network Summary: \033[92mAll {total_tests} tests passed - Internet connection is good\033[0m")
elif successful_connections > 0:
    log_print(f"Network Summary: \033[93m{successful_connections}/{total_tests} tests passed - Partial connectivity\033[0m")
else:
    log_print(f"Network Summary: \033[91mAll tests failed - No internet connection\033[0m")

# ------------------ GOOGLE RESPONSE TIME ------------------
try:
    start_time = time.time()
    sock = socket.create_connection(("google.com", 80), timeout=5)
    end_time = time.time()
    response_time = (end_time - start_time) * 1000
    sock.close()
    
    if response_time < 100:
        log_print(f"Response Time: \033[92m{response_time:.0f}ms to google.com [EXCELLENT]\033[0m")
    elif response_time < 300:
        log_print(f"Response Time: \033[93m{response_time:.0f}ms to google.com [GOOD]\033[0m")
    else:
        log_print(f"Response Time: \033[91m{response_time:.0f}ms to google.com [SLOW]\033[0m")
        
except Exception as e:
    log_print(f"Response Time: \033[91mCould not measure ({e})\033[0m")

# ------------------ WINDOWS SERVICE CHECKS ------------------
log_print("\n--- SERVICES ---")
services_to_check = [
    "RpcSs",             
    "wuauserv",          
    "mpssvc",            
    "WinDefend",         
    "Dhcp",              
    "Dnscache",          
    "LanmanWorkstation", 
    "BITS",              
    "LanmanServer",      
    "Spooler",           
    "Audiosrv",          
    "NlaSvc"             
]

if os_name == "Windows":
    services_running = 0
    total_services = len(services_to_check)

    for service_name in services_to_check:
        try:
            service = psutil.win_service_get(service_name)
            service_info = service.as_dict()
            status = service_info['status']
            
            if status == 'running':
                log_print(f"{service_info['display_name']}: \033[92mRunning \033[0m")
                services_running += 1
            else:
                log_print(f"{service_info['display_name']}: \033[91m{status.upper()} \033[0m")
        except Exception as e:
            log_print(f"{service_name}: \033[91mNot found \033[0m")
    log_print(f"Services Summary: \033[92m{services_running}/{total_services} services running\033[0m")
else:
    log_print("Service checks are only available on Windows.")

# ------------------ END OF REPORT ------------------
log_print("=" * 45)
log_print("                END OF REPORT       ")
log_print("=" * 45)

log_file.close()

