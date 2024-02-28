#!/usr/bin/env python3
import sys
import subprocess
from datetime import datetime

def file_type(file_path):
    return subprocess.check_output(['file', file_path]).decode()

def extract_metadata(file_path):
    # Placeholder for extracting metadata, can use exiftool, binwalk
    metadata = subprocess.check_output(['exiftool', file_path]).decode()
    return metadata

def main(file_path):
    analysis_results = f"## Forensics Analysis Report\n\n"
    analysis_results += f"### File Type Information\n```\n{file_type(file_path)}\n```\n\n"
    analysis_results += f"### Metadata\n```\n{extract_metadata(file_path)}\n```\n\n"
    
    # Save results to markdown
    filename = f"{file_path.split('/')[-1]}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"
    with open(filename, 'w') as f:
        f.write(analysis_results)
    print(filename)  # Print the filename for Ansible to fetch

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: forensics_analysis.py <file_path>")
        sys.exit(1)
    main(sys.argv[1])

