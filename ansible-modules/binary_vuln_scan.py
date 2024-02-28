#!/usr/bin/env python3
import subprocess
import sys
from datetime import datetime

# Expanded list of functions that could lead to vulnerabilities
vulnerable_functions = [
    'strcpy', 'strncpy',  # String copy functions without bounds checking
    'sprintf', 'vsprintf',  # Functions that write formatted output to strings without bounds checking
    'gets',  # Reads a line from stdin into a buffer without bounds checking
    'scanf', 'fscanf', 'sscanf',  # If not used carefully, can lead to overflow
    'strcat', 'strncat',  # Similar to strcpy but for concatenating strings
    'realpath',  # Can be dangerous if not used properly
    'getwd',  # Replaced by getcwd because of potential buffer overflows
    'system', 'popen'  # Can be dangerous if command includes user input
]

def is_binary_file(file_path):
    file_type = subprocess.run(['file', file_path], capture_output=True, text=True).stdout
    return 'executable' in file_type

def disassemble_binary(binary_path):
    result = subprocess.run(['objdump', '-D', '-M', 'intel', binary_path], capture_output=True, text=True)
    return result.stdout

def scan_for_vulnerabilities(disassembly):
    findings = []
    for function in vulnerable_functions:
        if function in disassembly:
            findings.append(f"Potential vulnerability found: usage of {function}")
    return findings

def save_to_markdown(binary_name, findings):
    filename = f"/home/ansible-modules/tmp/{binary_name}_vuln_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"
    with open(filename, 'w') as f:
        f.write(f"# Vulnerability Scan Results for {binary_name}\n")
        for finding in findings:
            f.write(f"- {finding}\n")
    return filename

if __name__ == '__main__':
    binary_path = sys.argv[1]
    if not is_binary_file(binary_path):
        print(f"The file at {binary_path} is not a binary executable.")
        sys.exit(1)
    binary_name = binary_path.split('/')[-1]
    disassembly = disassemble_binary(binary_path)
    findings = scan_for_vulnerabilities(disassembly)
    markdown_file = save_to_markdown(binary_name, findings)
    print(markdown_file)

