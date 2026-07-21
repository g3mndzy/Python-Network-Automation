import requests

HELPDESK_URL = "http://helpdesk.d522.wgu.internal:5000/api/tickets"

headers = {
    "Authorization": "Bearer vGkbXkGLqQSo7YLflp9DutuG8st4xdPPF7wnTcwB0FE",
    "Content-Type": "application/json"
}

ticket_data = {
    "title": "DNS Setting Altered - PC2",
    "description": (
        "Device Name: PC2\n"
        "IP Address: 192.168.20.100\n"
        "Issue Type: DNS Setting Altered\n\n"
        "An unauthorized DNS server was detected. "
        "Expected DNS server: 10.10.10.20."
    ),
    "priority": "high",
    "status": "open",
    "assigned_to": "Network Team",
    "requester_email": "gmen144@wgu.edu"
}

response = requests.post(
    HELPDESK_URL,
    headers=headers,
    json=ticket_data,
    timeout=10
)

if response.status_code in (200, 201):
    ticket = response.json()
    print("DNS ticket created successfully.")
    print("Ticket ID:", ticket["id"])
    print(ticket)
else:
    print("DNS ticket creation failed.")
    print("Status code:", response.status_code)
    print("Response:", response.text)