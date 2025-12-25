# System Health Check

## Description
Python script that generates a comprehensive system health report. It collects CPU, memory, disk usage, system uptime, network connectivity, response time, and Windows service status (if applicable). The output is displayed in the terminal with color-coded warnings and saved to a timestamped log file.

---

## Features

- System Information: OS, architecture, and computer hostname 
- CPU Usage: Current CPU usage with high usage warnings 
- Memory Usage: Current memory usage with high usage alerts 
- Disk Usage: Detailed disk space usage with low-space warnings 
- Network Connectivity: Tests connection to Google and Cloudflare 
- Response Time: Measures response time to google.com 
- Windows Services: Checks status of important Windows services (Windows only) 
- Color-Coded Output: Green/Yellow/Red warnings for easy monitoring 
- Error Handling: Gracefully handles inaccessible disks, network failures, or missing services 
- Automatic Logging: Saves a timestamped report in Logs/ 

## Prerequisites
- Python 3.x installed on your system 
- psutil Python library 
- Install psutil if not already installed:  
  - pip install psutil
 
## Setup & Usage
1. Download system_health_check.py from this repository.
2. Create a folder called Logs in the same directory as the script — the script will also create it automatically if it doesn’t exist. 
 <img width="595" height="583" alt="Screenshot 2025-09-20 163912" src="https://github.com/user-attachments/assets/47f17f59-d8a4-46cb-8b0a-74c452d3b59e" />

3. Open a terminal or command prompt. 
4. Navigate to the folder where the script is saved (if needed).  
<img width="428" height="40" alt="Screenshot 2025-09-20 163041" src="https://github.com/user-attachments/assets/b5bbc190-c3ab-4413-b5f4-399213fe6890" />

5. Run the script:
   - python system_health_check.py  
<img width="541" height="38" alt="Screenshot 2025-09-20 163128" src="https://github.com/user-attachments/assets/be64cdce-a374-4123-b93b-f3b78aafcf4f" />

6. Monitor the terminal for system health output.  
<img width="625" height="740" alt="Screenshot 2025-09-20 170639" src="https://github.com/user-attachments/assets/224d7af1-6e00-45ce-aa82-7efa23b71bdd" />

7. Check the Logs/ folder for the timestamped log file containing the full report.  
<img width="601" height="794" alt="Screenshot 2025-09-20 170742" src="https://github.com/user-attachments/assets/14cc27f9-e345-409d-b7d7-3b947444a703" />

## Output
The script provides: 

- Screen Output: Color-coded, real-time system status 
- Log File: Permanent record of system health metrics with timestamps 
- Alerts: Highlights high CPU/memory usage, low disk space, and network or service issues

## Notes

- Windows Services: Only checked on Windows systems. 
- Network Tests: May fail if firewalls block specific ports. 
- Logs: Automatically saved in Logs/ every time the script runs with timestamped filenames.

## License 
This project is licensed under the MIT License.
