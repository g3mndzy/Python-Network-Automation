
import csv

CSV_FILE = "network_devices.csv"


def main():
    with open(CSV_FILE, mode="r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        print("Network Devices")
        print("----------------")

        for row in reader:
            print(row["Device Name"])


if __name__ == "__main__":
    main()