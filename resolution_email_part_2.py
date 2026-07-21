import smtplib
from email.message import EmailMessage

AFFECTED_DEVICES = [
    {
        "name": "PC2",
        "host": "192.168.20.101",
    },
    {
        "name": "PC3",
        "host": "192.168.30.101",
    },
    {
        "name": "SVR1",
        "host": "192.168.20.210",
    },
    {
        "name": "SVR2",
        "host": "192.168.30.210",
    },
]


def send_resolution_email():

    sender_email = "gmen144@wgu.edu"
    receiver_email = "stakeholders@d522.wgu.internal"

    smtp_server = "smtp.d522.wgu.internal"
    smtp_port = 1025

    subject = "RESOLVED: DNS Service Issue and Device Compromise—All Issues Remediated"

    device_list = ""

    for device in AFFECTED_DEVICES:
        device_list += f"""
Device Name: {device["name"]}
IP Address: {device["host"]}
"""

    body = f"""
Dear Stakeholders,

This is an automated notification to inform you that the DNS service issue and all related device compromises have been successfully resolved. The following devices were affected and have now been remediated:

{device_list}

No further action is required at this time. If you have any questions or concerns, please contact the IT support team.

Thank you for your attention.

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

    print("Resolution notification email sent successfully.")


def main():
    send_resolution_email()


if __name__ == "__main__":
    main()