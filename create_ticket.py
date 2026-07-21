import requests

HELPDESK_URL = "http://helpdesk.d522.wgu.internal:5000/api/tickets"

headers = {
    "Authorization": "Bearer vGkbXkGLqQSo7YLflp9DutuG8st4xdPPF7wnTcwB0FE"
}

compromised_devices = [
    {"name": "PC2", "ip": "192.168.1.10", "issue": "Rogue DNS configuration", "service": "DNS"},
    {"name": "PC3", "ip": "192.168.1.11", "issue": "Rogue DNS configuration", "service": "DNS"},
    {"name": "SVR1", "ip": "192.168.1.20", "issue": "Rogue DNS configuration", "service": "DNS"},
    {"name": "SVR2", "ip": "192.168.1.21", "issue": "Rogue DNS configuration", "service": "DNS"},
]


def create_ticket(device):
    ticket_data = {
        "assigned_to": "Network Team",
        "description": (
            f"Device Name: {device['name']}\n"
            f"IP Address: {device['ip']}\n"
            f"Issue Type: {device['issue']}\n"
            f"Service: {device['service']}\n\n"
            "This device has been identified as compromised due to a rogue DNS configuration. "
            "Immediate investigation and remediation are recommended."
        ),
        "priority": "high",
        "requester_email": "gmen144@wgu.edu",
        "status": "open",
        "title": f"Compromised Device Detected - {device['name']}"
    }

    response = requests.post(
        HELPDESK_URL,
        json=ticket_data,
        headers=headers
    )

    if response.status_code == 201:
        print(f"Ticket created successfully for {device['name']}")
    else:
        print(f"Failed to create ticket for {device['name']}")
        print(f"Status code: {response.status_code}")
        print(response.text)


def main():
    for device in compromised_devices:
        create_ticket(device)


if __name__ == "__main__":
    main()