from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException
from netmiko.exceptions import NetmikoTimeoutException
from paramiko.ssh_exception import SSHException


CORRECT_DNS = "10.10.10.20"

AFFECTED_DEVICES = [
    {
        "name": "PC2",
        "host": "192.168.20.101",
        "username": "ubuntu",
        "password": "ubuntu",
    },
    {
        "name": "PC3",
        "host": "192.168.30.101",
        "username": "ubuntu",
        "password": "ubuntu",
    },
    {
        "name": "SVR1",
        "host": "192.168.20.210",
        "username": "ubuntu",
        "password": "ubuntu",
    },
    {
        "name": "SVR2",
        "host": "192.168.30.210",
        "username": "ubuntu",
        "password": "ubuntu",
    },
]


def run_sudo_command(connection, command, password):
    output = connection.send_command_timing(command)

    if "password" in output.lower():
        output += connection.send_command_timing(password)

    return output


def correct_dns(device):
    connection = None

    try:
        print("\n" + "=" * 60)
        print(f"Connecting to {device['name']} at {device['host']}")

        connection = ConnectHandler(
            device_type="linux",
            host=device["host"],
            username=device["username"],
            password=device["password"],
        )

        print("\nDNS settings before update:")
        before_output = connection.send_command("cat /etc/resolv.conf")
        print(before_output)

        print(f"\nUpdating DNS to {CORRECT_DNS}...")

        update_command = (
            f"echo 'nameserver {CORRECT_DNS}' | "
            "sudo tee /etc/resolv.conf"
        )

        update_output = run_sudo_command(
            connection,
            update_command,
            device["password"],
        )

        print("\nUpdate command output:")
        print(update_output)

        print("\nDNS settings after update:")
        after_output = connection.send_command("cat /etc/resolv.conf")
        print(after_output)

        if f"nameserver {CORRECT_DNS}" in after_output:
            print(
                f"\n[SUCCESS] {device['name']} DNS settings "
                "were updated successfully."
            )
        else:
            print(
                f"\n[WARNING] DNS update could not be verified "
                f"for {device['name']}."
            )

    except NetmikoAuthenticationException:
        print(f"[ERROR] Authentication failed for {device['name']}.")

    except NetmikoTimeoutException:
        print(f"[ERROR] Connection timed out for {device['name']}.")

    except Exception as error:
        print(f"[ERROR] {device['name']}: {error}")

    finally:
        if connection:
            connection.disconnect()


def main():
    for device in AFFECTED_DEVICES:
        correct_dns(device)


if __name__ == "__main__":
    main()
