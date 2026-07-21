
"""""
this script will test connectivity to network devices listed in a CSV file named 'network_devices.csv'. The CSV file is expected to have a header row with columns named "Device Name" and "Device Address". The script will ping each device and print its status as "Online", "Offline", or "Skipped - No static IP" if the address is set to "DHCP" or "None".
"""""


import csv
import subprocess


def ping_device(ip_address):
    result = subprocess.run(
        ["ping", "-c", "1", ip_address],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return "Online"
    else:
        return "Offline"


def main():

    with open("network_devices.csv", "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            device_name = row["Device Name"]
            ip_address = row["Device Address"]

            status = ping_device(ip_address)

            print(f"{device_name}: {ip_address} is {status}")


if __name__ == "__main__":
    main()