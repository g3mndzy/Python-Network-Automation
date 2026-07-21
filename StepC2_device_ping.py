"""
This script tests connectivity to network devices listed in
network_devices.csv.

The CSV file must contain columns named:
- Device Name
- Device Address

Devices with DHCP, None, or a blank address are skipped.
"""

import csv
import subprocess


def ping_device(ip_address):
    """Ping one device and return Online or Offline."""

    result = subprocess.run(
        ["ping", "-c", "1", "-W", "2", ip_address],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return "Online"

    return "Offline"


def main():
    with open("network_devices.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            device_name = row["Device Name"].strip()
            ip_address = row["Device Address"].strip()

            if ip_address.lower() in ("dhcp", "none", ""):
                print(
                    f"{device_name}: Skipped - No static IP"
                )
                continue

            status = ping_device(ip_address)

            print(
                f"{device_name}: {ip_address} is {status}"
            )


if __name__ == "__main__":
    main()