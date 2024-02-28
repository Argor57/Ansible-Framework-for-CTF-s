#!/usr/bin/env python3
import sys

def add_host(ip, name):
    hosts_file = '/etc/hosts'
    entry = f"{ip}\t{name}\n"

    try:
        with open(hosts_file, 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            found = False
            for line in lines:
                if name in line:
                    line = entry  # Replace the existing entry with the new one
                    found = True
                file.write(line)
            if not found:
                file.write(entry)  # Append the new entry at the end if not found
    except PermissionError:
        print("Permission denied: You need to run this script as root to modify /etc/hosts.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: add_host.py <IP Address> <Host Name>")
        sys.exit(1)

    ip_address = sys.argv[1]
    host_name = sys.argv[2]

    if add_host(ip_address, host_name):
        print(f"Host {host_name} with IP {ip_address} added or updated successfully.")
    else:
        print("Failed to add or update host.")
        sys.exit(1)



