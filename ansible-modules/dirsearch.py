#!/usr/bin/env python3
import subprocess
import sys
from datetime import datetime

def run_dirsearch(url):
    # Configure the dirsearch command
    command = ['dirsearch', '-u', url]

    # Execute dirsearch
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

def save_results(url, results):
    directory = "/home/pi/ansible-modules/tmp/"
    # Simplify URL to a filename-friendly format
    simplified_url = url.replace('://', '_').replace('/', '_')
    filename = f"{directory}{simplified_url}_dirsearch.md"

    with open(filename, 'w') as file:
        file.write(f"# Dirsearch Results for {url}\n\n")
        file.write("```text\n")
        file.write(results)
        file.write("\n```\n")
    
    return filename

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 dirsearch_wrapper.py <url>")
        sys.exit(1)

    target_url = sys.argv[1]
    dirsearch_output = run_dirsearch(target_url)
    output_file = save_results(target_url, dirsearch_output)

    # Print the absolute path to the output file
    print(output_file)

