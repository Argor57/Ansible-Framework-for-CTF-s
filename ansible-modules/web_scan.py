#!/usr/bin/env python3
import subprocess
import sys
from datetime import datetime

def run_nmap_scan(ip):
    # Configure scan arguments for a comprehensive scan
    args = ['nmap', '-sC', '-sV', '-O', '-A', '-T4', '-Pn', ip]
    
    scan_result = subprocess.run(args, capture_output=True, text=True)
    return scan_result.stdout

def write_to_markdown(ip, scan_results):
    # Ensure the directory exists
    directory = "/home/pi/ansible-modules/tmp/"
    filename = f"{directory}{ip}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"
    
    with open(filename, 'w') as f:
        f.write(f"# Nmap Scan Results for {ip}\n\n")
        f.write(f"## Comprehensive Scan\n```\n{scan_results}\n```\n")
    
    return filename

if __name__ == '__main__':
    ip_address = sys.argv[1]

    # Execute the comprehensive nmap scan
    scan_results = run_nmap_scan(ip_address)
    markdown_file = write_to_markdown(ip_address, scan_results)
    
    scan_results = run_nmap_scan(ip_address)
    markdown_file = write_to_markdown(ip_address, scan_results)
    
    print(markdown_file)

