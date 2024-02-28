#!/usr/bin/env python3

from datetime import datetime
import json
import os

def main():
    # Define the path to save the datetime file
    datetime_file = '/home/pi/ansible-modules/tmp/current_datetime.txt'
    
    # Get current datetime
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Ensure the tmp directory exists
    os.makedirs(os.path.dirname(datetime_file), exist_ok=True)

    # Write the current datetime to the file
    with open(datetime_file, 'w') as file:
        file.write(current_datetime)
    
    # Prepare the module output
    result = {
        "changed": True,
        "datetime": current_datetime,
        "message": f"Current datetime written to {datetime_file}"
    }
    print(json.dumps(result))

if __name__ == '__main__':
    main()

