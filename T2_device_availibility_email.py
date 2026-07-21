

import csv
import smtplib
from datetime import datetime
from email.message import EmailMessage

from StepC2_device_ping import ping_device


CSV_FILE = "network_devices.csv"

SMTP_SERVER = "smtp.d522.wgu.internal"
SMTP_PORT = 1025

SENDER_EMAIL = "gmen144@wgu.edu"
RECEIVER_EMAIL = "stakeholders@d522.wgu.internal"


def send_unavailable_email(device_name, ip_address):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = EmailMessage()
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = (
        f"Network Device Unavailable: "
        f"{device_name} ({ip_address})"
    )

    message.set_content(
        f"""Dear Network Administrator,

This is an automated notification that the following network device is currently unavailable:

Device Name: {device_name}
IP Address: {ip_address}
Last Checked: {timestamp}

Please investigate this issue at your earliest convenience.

Best regards,
Network Monitoring System
"""
    )

    try:
        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT,
            timeout=10
        ) as server:
            server.send_message(message)

        print(f"Email sent for {device_name}.")
        return True

    except (smtplib.SMTPException, OSError) as error:
        print(f"Email failed for {device_name}: {error}")
        return False


def main():
    with open(
        CSV_FILE,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            device_name = row["Device Name"].strip()
            ip_address = row["Device Address"].strip()

            if ip_address.lower() in {
                "dhcp",
                "none",
                "n/a",
                ""
            }:
                print(
                    f"{device_name}: "
                    "Skipped - No static IP"
                )
                continue

            status = ping_device(ip_address)

            print(
                f"{device_name}: "
                f"{ip_address} is {status}"
            )

            if status == "Offline":
                send_unavailable_email(
                    device_name,
                    ip_address
                )


if __name__ == "__main__":
    main()