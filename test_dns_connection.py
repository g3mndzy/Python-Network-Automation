import csv
from netmiko import ConnectHandler
from ping_devices import ping_device
from paramiko.ssh_exception import SSHException


def get_dns(ip_address, username, password):
    device = {
        "device_type": "linux",
        "host": ip_address,
        "username": username,
        "password": password,
    }

    try:
        connection = ConnectHandler(**device)
        output = connection.send_command("cat /etc/resolv.conf")
        connection.disconnect()
        return output

    except SSHException:
        return "SSH connection failed or timed out."

    except Exception as error:
        return f"Unexpected error: {error}"


def main():
    with open("network_devices.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            device_name = row["Device Name"]
            ip_address = row["Device Address"]
            username = row["Username"]
            password = row["Password"]

            status = ping_device(ip_address)

            print(f"\n{device_name}: {status}")

            if status == "Online":
                dns_output = get_dns(
                    ip_address,
                    username,
                    password
                )

                print("Current DNS configuration:")
                print(dns_output)


if __name__ == "__main__":
    main()