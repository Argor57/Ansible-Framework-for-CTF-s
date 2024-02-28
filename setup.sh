#!/bin/bash

# Update and upgrade apt packages
apt-get update && apt-get upgrade -y

# Install ansible
apt-get install ansible -y

# Install general tools
apt-get install -y nmap git wireshark gdb docker.io sqlmap nmap netcat-traditional binwalk tcpdump openvpn john hashcat sleuthkit binwalk dirsearch openvpn wfuzz rsync  # add any additional apt packages here

# Install Python modules
# pip3 install pwntools 
apt-get install python3-full -y
apt-get install python3-pip -y
apt-get install python3-pwntools -y
apt-get install python3-volatility -y
apt-get install python3-volatility3 -y
apt-get install python3-magic -y

# Download and install Burp Suite Community Edition
# wget -O /tmp/burpsuite_community.sh "INPUT BURPSUITE DOWNLOAD LINK HERE"
# chmod +x /tmp/burpsuite_community.sh
# sh /tmp/burpsuite_community.sh -q

# Install Ghidra
# wget -O /tmp/ghidra.zip "INPUT GHIDRA DOWNLOAD LINK HERE"
# unzip /tmp/ghidra.zip -d /opt/
# export JAVA_HOME="/usr/lib/jvm/default-java"

# Define the directory for wordlists
DIR="/home/pi/wordlists"

# Create the target directory if it doesn't exist
mkdir -p "$DIR"

# Navigate to the target directory
cd "$DIR"

# List of repositories to clone
REPOS=(
    "https://github.com/danielmiessler/SecLists.git"
    "https://github.com/danielmiessler/RobotsDisallowed.git"
    "https://github.com/fuzzdb-project/fuzzdb.git"
)

# Clone each repository
for repo in "${REPOS[@]}"; do
    echo "Cloning $repo into $TARGET_DIR"
    git clone "$repo"
done

echo "All repositories have been cloned into $TARGET_DIR."
