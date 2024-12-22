import socket
import os
import ipaddress
from scapy.all import ARP, Ether, srp

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception as e:
        print(f"Fout bij ophalen van lokaal IP: {e}")
        return "127.0.0.1"

def scan_network(subnet):
    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=2, verbose=False)[0]
    active_hosts = []
    for _, received in result:
        active_hosts.append(received.psrc)
    return active_hosts

def save_results_to_file(hostname, results):
    directory = f"./data/{hostname}"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, "nmap_results.txt")
    with open(file_path, "w") as f:
        for ip in results:
            f.write(f"{ip}\n")

def run():
    hostname = socket.gethostname()
    local_ip = get_local_ip()
    try:
        # Bereken het subnet door het IP-adres af te ronden naar het netwerk (CIDR /24)
        network = ipaddress.ip_network(local_ip + "/24", strict=False)
        subnet = str(network)
        print(f"Scannen van subnet: {subnet}")
        
        active_hosts = scan_network(subnet)
        # save_results_to_file(hostname, active_hosts)
        return {"status": "success", "active_hosts": active_hosts}
    except Exception as e:
        print(f"Fout bij uitvoeren van netwerk-scan: {e}")
        return {"status": "error", "message": str(e)}
