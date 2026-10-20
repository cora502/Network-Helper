# device_name=input("enter your device name ")
# ip_address=input('enter your ip address ')
# print("Network information")
# print("device name "+device_name)
# print("ip address "+ip_address)


import subprocess
from datetime import datetime
import ipaddress

def show_summary():
    try:
        with open("network_report.txt", "r", encoding="utf-8") as file:
            report = file.read()

        if not report.strip():
            print("No test results available.")
            return

        successful = report.count("Status: Ping response received")
        unsuccessful = report.count("Status: No successful ping response detected")
        timed_out = report.count("Status: Ping timed out")

        print("\n===== Network Test Summary =====")
        print("Successful tests:", successful)
        print("Unsuccessful tests:", unsuccessful)
        print("Timed-out tests:", timed_out)
        print("Total recorded results:", successful + unsuccessful + timed_out)

    except FileNotFoundError:
        print("No report found. Test an IP address first.")

def view_report():
    try:
        with open("network_report.txt", "r", encoding="utf-8") as file:
            report = file.read()

        if report.strip():
            print("\n===== Network Test History =====")
            print(report)
        else:
            print("The report file is empty.")

    except FileNotFoundError:
        print("No report found. Test an IP address first.")

def save_report(host, status, timestamp):
    """Save one network test result to a report file."""
    with open("network_report.txt", "a", encoding="utf-8") as file:
        file.write(f"Time: {timestamp}\n")
        file.write(f"Host tested: {host}\n")
        file.write(f"Status: {status}\n")
        file.write("-" * 30 + "\n")

    print("Report saved to network_report.txt")

def is_valid_ipv4(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


def check_host(host):
    try:
        result = subprocess.run(
            ["ping", "-n", "4", host],
            capture_output=True,
            text=True,
            timeout=10
        )

        print("\n--- Ping Result ---")
        print(result.stdout)

        if result.returncode == 0:
            status = "Ping response received"
        else:
            status = "No successful ping response detected"

    except subprocess.TimeoutExpired:
        status = "Ping timed out"
        print("The ping command took too long.")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Status:", status)

    save_report(host, status, timestamp)


# Main program

while True:
    print("\n===== Network Helper =====")
    print("1. Test an IP address")
    print("2. Exit")
    print("3. View report history")
    print("4. Show test summary")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        target = input("Enter an IPv4 address to test: ").strip()

        if not target:
            print("Please enter an IP address.")
        elif not is_valid_ipv4(target):
            print("Invalid IPv4 address. Please try again.")
        else:
            check_host(target)

    elif choice == "2":
        print("Exiting Network Helper. Goodbye!")
        break

    elif choice == "3":
        view_report()
    elif choice == "4":
        show_summary()

    else:
        print("Invalid choice. Please enter 1, 2, or 3 or 4.")