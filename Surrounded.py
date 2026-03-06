import scapy.all as scapy
import argparse
import requests
import csv
import os

# ─────────────────────────────────────────────
# get flags
# ─────────────────────────────────────────────
def get_arguments():
    parser = argparse.ArgumentParser(
        description="Surrounded - ARP network scanner"
    )
    parser.add_argument(
        "-t", "--target",
        dest="target",
        help="Target IP / IP range (e.g. 192.168.1.1/24)"
    )
    parser.add_argument(
        "-o", "--output",
        dest="output",
        help="Export results to file. Use .csv or .txt extension (e.g. results.csv)"
    )
    options = parser.parse_args()

    if not options.target:
        print("[-] Please specify a target IP range. Use --help for more info.")
        exit()
    return options


# ─────────────────────────────────────────────
# vendor lookup via macvendors.com API
# ─────────────────────────────────────────────
def get_vendor(mac: str) -> str:
    """Return vendor name for a MAC address using the macvendors.com public API."""
    try:
        url = f"https://api.macvendors.com/{mac}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text.strip()
        return "Unknown"
    except requests.RequestException:
        return "Unknown"


# ─────────────────────────────────────────────
# scan
# ─────────────────────────────────────────────
def scan(ip: str) -> list[dict]:
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=3, retry=2, verbose=False)[0]

    clients_list = []
    for sent, received in answered_list:
        mac = received.hwsrc
        print(f"  [+] Found {received.psrc} — looking up vendor for {mac}...")
        vendor = get_vendor(mac)
        client_dict = {"ip": received.psrc, "mac": mac, "vendor": vendor}
        clients_list.append(client_dict)
    return clients_list


# ─────────────────────────────────────────────
# print pretty result
# ─────────────────────────────────────────────
def print_result(results_list: list[dict]):
    col_w = 20
    header = f"{'IP Address':<{col_w}}{'MAC Address':<{col_w}}Vendor"
    sep = "-" * 70
    print(f"\n{sep}")
    print(header)
    print(sep)
    for client in results_list:
        print(f"{client['ip']:<{col_w}}{client['mac']:<{col_w}}{client['vendor']}")
    print(f"{sep}\n")


# ─────────────────────────────────────────────
# export results
# ─────────────────────────────────────────────
def export_results(results_list: list[dict], filepath: str):
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".csv":
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["ip", "mac", "vendor"])
            writer.writeheader()
            writer.writerows(results_list)
        print(f"[✓] Results exported to CSV: {filepath}")

    elif ext == ".txt":
        col_w = 20
        sep = "-" * 70
        with open(filepath, "w") as f:
            f.write(f"{sep}\n")
            f.write(f"{'IP Address':<{col_w}}{'MAC Address':<{col_w}}Vendor\n")
            f.write(f"{sep}\n")
            for client in results_list:
                f.write(f"{client['ip']:<{col_w}}{client['mac']:<{col_w}}{client['vendor']}\n")
            f.write(f"{sep}\n")
        print(f"[✓] Results exported to TXT: {filepath}")

    else:
        print(f"[-] Unsupported file extension '{ext}'. Use .csv or .txt")


# ─────────────────────────────────────────────
# execute
# ─────────────────────────────────────────────
if __name__ == "__main__":
    options = get_arguments()
    print(f"[*] Scanning network: {options.target} ...")
    scan_result = scan(options.target)
    print_result(scan_result)

    if options.output:
        export_results(scan_result, options.output)
