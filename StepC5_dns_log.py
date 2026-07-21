import csv
import re
from datetime import datetime
from test_dns_connection import get_dns


LOG_FILE = "dns_status.log"

APPROVED_DNS_SERVERS = {
    "10.10.10.10",
    "10.10.10.20"
}


def extract_dns_servers(dns_output):
    

    if not dns_output:
        return []

    return re.findall(
        r"nameserver\s+(\d{1,3}(?:\.\d{1,3}){3})",
        dns_output
    )


def dns_is_correct(dns_output):
    

    detected_dns_servers = extract_dns_servers(dns_output)

    if not detected_dns_servers:
        return False

    return all(
        dns_server in APPROVED_DNS_SERVERS
        for dns_server in detected_dns_servers
    )


def write_log(device_name, dns_servers):
    """Record a successful DNS check in the log file."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dns_list = ", ".join(dns_servers)

    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(
            f"{timestamp} | Device: {device_name} | "
            f"DNS: {dns_list} | "
            "DNS service is functioning correctly and has not been altered.\n"
        )


def main():
    with open(
        "network_devices.csv",
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as csv_file:

        reader = csv.DictReader(csv_file)

        for row in reader:
            device_name = row["Device Name"].strip()
            ip_address = row["Device Address"].strip()
            username = row["Username"].strip()
            password = row["Password"].strip()

            dns_output = get_dns(
                ip_address,
                username,
                password
            )

            detected_dns_servers = extract_dns_servers(dns_output)

            if dns_is_correct(dns_output):
                print(
                    f"{device_name}: DNS is correct "
                    f"({', '.join(detected_dns_servers)})"
                )

                write_log(
                    device_name,
                    detected_dns_servers
                )

            else:
                detected_value = (
                    ", ".join(detected_dns_servers)
                    if detected_dns_servers
                    else "No DNS server detected"
                )

                print(
                    f"{device_name}: DNS setting is altered or invalid. "
                    f"Detected: {detected_value}"
                )


if __name__ == "__main__":
    main()