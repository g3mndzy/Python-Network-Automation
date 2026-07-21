import smtplib
from datetime import datetime
from email.message import EmailMessage


SMTP_SERVER = "smtp.d522.wgu.internal"
SMTP_PORT = 1025

SENDER_EMAIL = "gmen144@wgu.edu"
STAKEHOLDER_EMAIL = "stakeholders@d522.wgu.internal"


def send_dns_altered_email(
    device_name,
    ip_address,
    current_dns,
    expected_dns
):
    """Send an email when an unauthorized DNS setting is detected."""

    message = EmailMessage()

    message["From"] = SENDER_EMAIL
    message["To"] = STAKEHOLDER_EMAIL
    message["Subject"] = f"DNS Setting Altered Notification - {device_name}"

    detected_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message.set_content(
        f"""
DNS SETTING ALTERED NOTIFICATION

An unauthorized DNS configuration has been detected.

Device Name: {device_name}
IP Address: {ip_address}
Detected DNS Setting: {current_dns}
Expected DNS Setting: {expected_dns}
Detection Time: {detected_time}

The DNS configuration will be corrected, and the associated support
ticket will be updated after the issue has been resolved.
"""
    )

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.send_message(message)

        print(f"[SUCCESS] DNS altered notification sent for {device_name}.")
        return True

    except Exception as error:
        print(f"[ERROR] Email could not be sent: {error}")
        return False


def main():
    
    send_dns_altered_email(
        device_name="PC2",
        ip_address="192.168.20.100",
        current_dns="203.0.113.10",
        expected_dns="10.10.10.20"
    )


if __name__ == "__main__":
    main()