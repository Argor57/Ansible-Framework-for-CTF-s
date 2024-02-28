import subprocess
import sys
import os
from urllib.parse import urlparse

def sanitize_filename(filename):
    """
    Sanitizes the filename by replacing invalid characters and
    potentially problematic characters with underscores.
    """
    return "".join([c if c.isalnum() or c in "._-" else "_" for c in filename])

def download_full_website(url, base_destination_path="/home/pi/websites"):
    # Parse the URL to create a directory name based on the domain and path
    parsed_url = urlparse(url)
    directory_name = sanitize_filename(parsed_url.netloc + parsed_url.path)

    # Construct the full path for the destination directory
    full_destination = os.path.join(base_destination_path, directory_name)

    # Ensure the destination directory exists
    if not os.path.exists(full_destination):
        os.makedirs(full_destination)

    # Use wget to download the full website
    command = ['wget', '-p', '-k', '-E', '-nd', '-P', full_destination, url]
    try:
        subprocess.run(command, check=True)
        print(f"Website and resources downloaded successfully to {full_destination}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading website: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]

    download_full_website(url)

