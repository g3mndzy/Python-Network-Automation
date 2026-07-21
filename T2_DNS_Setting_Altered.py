from netmiko import ConnectHandler

CORRECT_DNS_SERVER = "10.10.10.20"

device = {
    "device_type": "linux",
    "host": "192.168.20.100",
    "username": "ubuntu",
    "password": "ubuntu",
}

try:
    connection = ConnectHandler(**device)

    print("Connected to PC2")

    print("\nCurrent DNS:")
    print(connection.send_command("cat /etc/resolv.conf"))

    connection.send_command(
        f"echo 'nameserver {CORRECT_DNS_SERVER}' | sudo tee /etc/resolv.conf"
    )

    print("\nUpdated DNS:")
    print(connection.send_command("cat /etc/resolv.conf"))

    connection.disconnect()

except Exception as error:
    print(error)