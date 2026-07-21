from netmiko import ConnectHandler


def restart_dns(ip_address, username, password):
    device = {
        "device_type": "linux",
        "host": ip_address,
        "username": username,
        "password": password,
    }

    connection = ConnectHandler(**device)

    print("Restarting DNS service...")
    connection.send_command_timing("sudo systemctl restart named.service")

    print("\nChecking DNS service status...")
    status = connection.send_command("systemctl status named.service")
    print(status)

    if "active (running)" in status:
        print("\nDNS service is up and running.")
    else:
        print("\nDNS service is not running.")

    connection.disconnect()


def main():
    restart_dns("10.10.10.20", "ubuntu", "ubuntu")


if __name__ == "__main__":
    main()