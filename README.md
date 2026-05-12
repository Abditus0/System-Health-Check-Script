# System Health Check Script

A Python script that pulls a snapshot of system health and prints it to the terminal with color-coded warnings. CPU, memory, disk, uptime, network connectivity, response time to google.com, and the status of key Windows services. Every run also gets saved to a timestamped log file so you can compare runs over time or come back and check what was happening on a specific day.

I wrote this because I wanted a fast way to check the health of a machine without opening Task Manager, then Resource Monitor, then a browser to test connectivity, then Services.msc. One script, one run, everything in one place. Green when it's fine, yellow when something is worth watching, red when something needs attention.

## What it checks

| Check | What it does |
|-------|--------------|
| System info | OS, architecture, hostname |
| CPU | Current usage, flags anything above the warning threshold |
| Memory | Current usage, flags high pressure |
| Disk | Usage per drive, flags drives running low on space |
| Uptime | How long the system has been running since last boot |
| Network | Tests connectivity to Google and Cloudflare |
| Response time | Pings google.com and reports the response time |
| Windows services | Checks the status of important Windows services (Windows only) |

If a check fails (a disk is inaccessible, a service is missing, the network is down) the script logs the failure and keeps running. One failed check doesn't kill the rest of the report.

## What a run looks like

The terminal output is color-coded so you can read it at a glance. Green is fine, yellow is worth watching, red is a problem.

<img width="625" height="740" alt="Color-coded terminal output" src="https://github.com/user-attachments/assets/4d26def6-ce84-4c6f-98dd-4ca2fe77a7f1">

Every run also writes a timestamped log file to a `Logs/` folder next to the script. The folder gets created automatically on first run if it doesn't exist.

<img width="595" height="583" alt="Logs folder with timestamped files" src="https://github.com/user-attachments/assets/9f993de0-5688-4ac3-ada3-9bcb32d9c87e">

The log file has the full report in plain text without the color codes, so it's easy to grep through later or attach to a ticket.

<img width="601" height="794" alt="Log file contents" src="https://github.com/user-attachments/assets/d56aa7d2-2f32-467f-9577-3a86c57b3d1b">

## How to use it

```bash
pip install psutil
python system_health_check.py
```

That's it. The script prints the report to the terminal and drops a copy in `Logs/`. Runs on any system with Python 3 and `psutil`. Windows services check only runs on Windows; on Linux or macOS that section is skipped.

## Problems I had to solve

**Inaccessible disks crashing the script.** First version would die if `psutil` hit a disk it couldn't read (CD drive with no disc, an unmounted partition, a network drive that disconnected). Wrapped the per-disk check in try/except so an unreadable disk gets logged as an error and the script moves on to the next one.

**Network test that hung the whole script.** Originally I used a basic `requests.get()` with no timeout to test connectivity. If the network was up but slow, or if there was a DNS issue, the script would just sit there for 30+ seconds waiting. Added an explicit timeout so a failed network test fails fast instead of stalling everything else.

**Color codes leaking into the log file.** Terminal color codes look great in the terminal and look like garbage in a text file (`\033[92m` everywhere). First version wrote the same string to both. Fixed it by keeping two versions of each line: one with color for the terminal, one plain for the log. Now the log is clean text you can grep or paste into a ticket.

## What I learned

The thing that stuck with me is how much of monitoring is about thresholds, not measurements. Reading CPU usage is one line. Deciding what counts as "high" is the actual work. Same with disk space (10% free? 5%? depends on the drive size), memory pressure, response time. Numbers without thresholds are just numbers.

A few other things:

- `psutil` is the right tool for this on every OS. Cross-platform, well-maintained, doesn't require admin rights for most checks.
- ANSI color codes work in Windows Terminal and modern PowerShell but not in old `cmd.exe`. If you support older shells, you need a library like `colorama` to handle the translation.
- Always log to a file with a timestamp in the filename, not a single rolling log. Disk space is cheap, history is expensive to recover.
- Wrap every external call (network, disk, services) in its own try/except. Anything that can fail will fail at the worst time.

## Why I built it

Manual system health checks waste time. Every IT person ends up clicking through the same Task Manager → Resource Monitor → ping test → Services.msc loop. This script does the whole loop in one run and saves the output. Useful for the moment you suspect something is off, useful as a baseline before changes, useful as evidence after the fact.
