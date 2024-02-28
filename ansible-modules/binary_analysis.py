#!/usr/bin/env python3
import subprocess
import sys
from datetime import datetime

def is_binary_file(file_path):
    file_type = subprocess.run(['file', file_path], capture_output=True, text=True).stdout
    return 'executable' in file_type

def disassemble_binary(binary_path):
    # Ensure gdb uses Intel syntax for disassembly
    gdb_commands = f"set disassembly-flavor intel\nfile {binary_path}\ndisassemble\nquit"
    result = subprocess.run(['gdb', '--batch', '-ex', gdb_commands], capture_output=True, text=True)
    return result.stdout

def save_to_markdown(binary_name, disassembly):
    filename = f"/home/ansible-modules/tmp/{binary_name}_analysis_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"
    with open(filename, 'w') as f:
        f.write(f"# Disassembly Results for {binary_name}\n```assembly\n{disassembly}\n```")
    return filename

if __name__ == '__main__':
    binary_path = sys.argv[1]
    if not is_binary_file(binary_path):
        print(f"The file at {binary_path} is not a binary executable.")
        sys.exit(1)
    binary_name = binary_path.split('/')[-1]
    disassembly = disassemble_binary(binary_path)
    markdown_file = save_to_markdown(binary_name, disassembly)
    print(markdown_file)

