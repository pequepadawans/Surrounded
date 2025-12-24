import scapy.all as scapy
import argparse

# get flags
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range (e.g. 192.168.1.1/24)")
    options = parser.parse_args()
    
    if not options.target:
        print("[-] Please specify a target IP range. Use --help for more info.")
        exit()
    return options

# scan
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=3, retry=2, verbose=False)[0]

    # store as list
    clients_list = []
    for sent, received in answered_list:
        client_dict = {"ip": received.psrc, "MAC": received.hwsrc}
        clients_list.append(client_dict)
    return clients_list

# print pretty result
def print_result(results_list):
    print("\n" + "-"*50)
    print("IP Address\t\tMAC Address")
    print("-"*50)
    for client in results_list:
        print(f"{client['ip']}\t\t{client['MAC']}")
    print("-" * 50 + "\n")

# execute
if __name__ == "__main__":
    options = get_arguments()
    print(f"[*] Scanning network: {options.target} ...")
    scan_result = scan(options.target)
    print_result(scan_result)
