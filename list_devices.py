"""
This script reads a CSV file named 'network_devices.csv' and prints the "Device Name" of each device listed in the file. The CSV file is expected to have a header row with a column named "Device Name".
"""

import csv

with open('network_devices.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row["Device Name"])
              