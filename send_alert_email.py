import csv
import smtplib
from email.message import EmailMessage
from datetime import datetime
from test_dns_connection import get_dns
from ping_devices import ping_device


def has_rogue_dns(dns_output):
    return "203." in dns_output


def send_alert_email(compromised_devices):
    sender_email = "gmen144@wgu.edu"
    receiver_email = "stakeholders@d522.wgu.internal"

    smtp_server = "smtp.d522.wgu.internal"
    smtp_port = 1025

    subject = "URGENT: Device Compromise Detected—Immediate Attention Required"

    device_list = ""

    for device in compromised_devices:
        device_list += f"""
Device Name: {device["device_name"]}
IP Address: {device["ip_address"]}
Service: {device["service"]}
Last Checked: {device["last_checked"]}
"""

    body = f"""
Dear Stakeholders,

This is an automated alert to inform you that the following device(s) have been identified as compromised during the recent network scan:

{device_list}

Immediate investigation and remediation are recommended to prevent further impact.

If you have any questions or require additional information, please contact the IT support team.

Best regards,
Network Monitoring System
"""

    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.send_message(message)

    print("Alert email sent for all compromised devices.")


def main():
    compromised_devices = []

    with open("network_devices.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            device_name = row["Device Name"]
            ip_address = row["Device Address"]
            username = row["Username"]
            password = row["Password"]

            status = ping_device(ip_address)

            if status == "Online":
                dns_output = get_dns(ip_address, username, password)

                if has_rogue_dns(dns_output):
                    print(f"Rogue DNS detected on {device_name}")

                    compromised_devices.append({
                        "device_name": device_name,
                        "ip_address": ip_address,
                        "service": "DNS",
                        "last_checked": datetime.now()
                    })
                else:
                    print(f"{device_name}: DNS is normal")
            else:
                print(f"{device_name}: Offline")

    if compromised_devices:
        send_alert_email(compromised_devices)
    else:
        print("No compromised devices found.")


if __name__ == "__main__":
    main()