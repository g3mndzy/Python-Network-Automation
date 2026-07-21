import csv
import requests

from ping_devices import ping_device


HELPDESK_URL = "http://helpdesk.d522.wgu.internal:5000/api/tickets"

headers = {
    "Authorization": "Bearer vGkbXkGLqQSo7YLflp9DutuG8st4xdPPF7wnTcwB0FE"
}


def create_ticket(device_name, ip_address):
    ticket_data = {
        "assigned_to": "Network Team",
        "description": (
            f"Device Name: {device_name}\n"
            f"IP Address: {ip_address}\n"
            f"Issue Type: Device Unavailable\n\n"
            "This device did not respond to the network availability check. "
            "Please investigate the device at your earliest convenience."
        ),
        "priority": "high",
        "requester_email": "gmen144@wgu.edu",
        "status": "open",
        "title": f"Network Device Unavailable - {device_name}"
    }

    print(f"Attempting to create ticket for {device_name}...")

    try:
        response = requests.post(
            HELPDESK_URL,
            json=ticket_data,
            headers=headers,
            timeout=10
        )

        if response.status_code == 201:
            print(
                f"[TICKET CREATED] Ticket created successfully for "
                f"{device_name} ({ip_address})"
            )
            return True

        print(f"[TICKET FAILED] Could not create ticket for {device_name}")
        print(f"Status code: {response.status_code}")
        print(f"Server response: {response.text}")
        return False

    except requests.RequestException as error:
        print(f"[CONNECTION ERROR] {error}")
        return False


def main():
    devices_checked = 0
    unavailable_devices = 0
    tickets_created = 0

    print("Starting device availability check...")
    print("-------------------------------------")

    try:
        with open(
            "network_devices.csv",
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                device_name = row["Device Name"].strip()
                ip_address = row["Device Address"].strip()

                if ip_address.upper() in {"DHCP", "NONE", "N/A", ""}:
                    print(
                        f"[SKIPPED] {device_name}: "
                        "No usable IP address listed."
                    )
                    continue

                devices_checked += 1

                print(f"\nChecking {device_name} at {ip_address}...")

                status = ping_device(ip_address)

                if status == "Online":
                    print(
                        f"[AVAILABLE] {device_name} "
                        f"({ip_address}) is online."
                    )

                else:
                    unavailable_devices += 1

                    print(
                        f"[UNAVAILABLE DETECTED] {device_name} "
                        f"({ip_address}) is offline."
                    )

                    if create_ticket(device_name, ip_address):
                        tickets_created += 1

    except FileNotFoundError:
        print("[ERROR] network_devices.csv was not found.")
        return

    except KeyError as error:
        print(f"[ERROR] Missing CSV column: {error}")
        return

    print("\n-------------------------------------")
    print("Availability and ticket check completed.")
    print(f"Devices checked: {devices_checked}")
    print(f"Unavailable devices detected: {unavailable_devices}")
    print(f"Tickets created: {tickets_created}")

    if unavailable_devices == 0:
        print(
            "[RESULT] No unavailable devices were detected, "
            "so no tickets were created."
        )

    elif tickets_created == unavailable_devices:
        print(
            "[RESULT] A ticket was successfully created for "
            "every unavailable device."
        )

    else:
        print(
            "[RESULT] One or more unavailable-device tickets "
            "failed to create."
        )


if __name__ == "__main__":
    main()