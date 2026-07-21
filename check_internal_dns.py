from netmiko import ConnectHandler

dns_servers = [
    {
        "name": "DNS1",
        "device_type": "linux",
        "host": "10.10.10.10",
        "username": "ubuntu",
        "password": "ubuntu",
    },
    {
        "name": "DNS2",
        "device_type": "linux",
        "host": "10.10.10.20",
        "username": "ubuntu",
        "password": "ubuntu",
    }
]

def check_dns_service(server):

    print(f"\nChecking {server['name']}...")

    device = {
        "device_type": server["device_type"],
        "host": server["host"],
        "username": server["username"],
        "password": server["password"],
    }

    connection = ConnectHandler(**device)

    output = connection.send_command("systemctl status named")

    print(output)

    connection.disconnect()

def main():

    for server in dns_servers:
        check_dns_service(server)


if __name__ == "__main__":
    main()

