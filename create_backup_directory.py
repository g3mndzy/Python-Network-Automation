import csv
from pathlib import Path

from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)

from ping_devices import ping_device


BACKUP_FOLDER = Path("DNS-Backup")


def get_dns_config(ip_address, username, password):
    device = {
        "device_type": "linux",
        "host": ip_address,
        "username": username,
        "password": password,
    }

    try:
        connection = ConnectHandler(**device)

        command = (
    'echo "===== /etc/bind/named.conf ====="; '
    'cat /etc/bind/named.conf; '
    'echo; '
    'echo "===== /etc/bind/named.conf.local ====="; '
    'cat /etc/bind/named.conf.local; '
    'echo; '
    'echo "===== SLAVE DNS RECORDS ====="; '
    'named-compilezone -f raw -F text '
    '-o - '
    'd522.wgu.internal '
    '/var/cache/bind/db.d522.wgu.internal'
)

        output = connection.send_command_timing(
            command,
            read_timeout=90
        )

        connection.disconnect()
        return output

    except NetmikoAuthenticationException:
        return "Authentication failed."

    except NetmikoTimeoutException:
        return "SSH connection failed or timed out."

    except Exception as error:
        return f"Unexpected error: {repr(error)}"


def save_dns_backup(server_number, device_name, ip_address, config):

    server_folder = BACKUP_FOLDER / f"Server-{server_number}"
    server_folder.mkdir(parents=True, exist_ok=True)

    backup_file = server_folder / "record-config.txt"

    backup_contents = (
        f"DNS Server: {device_name}\n"
        f"IP Address: {ip_address}\n"
        f"{'=' * 50}\n\n"
        f"{config}\n"
    )

    backup_file.write_text(backup_contents, encoding="utf-8")

    print(f"Backup created: {backup_file}")


def main():
    BACKUP_FOLDER.mkdir(exist_ok=True)

    dns_server_number = 1

    with open(
        "network_devices.csv",
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            device_name = row["Device Name"].strip()
            ip_address = row["Device Address"].strip()
            username = row["Username"].strip()
            password = row["Password"].strip()

            if "DNS" not in device_name.upper():
                continue

            print(f"\nChecking {device_name} at {ip_address}...")

            status = ping_device(ip_address)

            print(f"{device_name}: {status}")

            if status != "Online":
                print(f"Skipping {device_name} because it is offline.")
                continue

            dns_config = get_dns_config(
                ip_address,
                username,
                password,
            )

            save_dns_backup(
                dns_server_number,
                device_name,
                ip_address,
                dns_config,
            )

            dns_server_number += 1

            # Stop after backing up two DNS servers.
            if dns_server_number > 2:
                break

    if dns_server_number <= 2:
        print("\nWarning: Two DNS servers were not successfully backed up.")
    else:
        print("\nBoth DNS server backups were created successfully.")


if __name__ == "__main__":
    main()