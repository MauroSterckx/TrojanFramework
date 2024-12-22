import os
import socket
import json

def run():
    try:
        # Bepaal lokaal subnet
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        subnet = ".".join(local_ip.split('.')[:3])  # Neem de eerste 3 octetten, bijvoorbeeld: 192.168.1

        print(f"Netwerkverkenning gestart voor subnet: {subnet}.x")

        # Vind actieve hosts
        active_hosts = []
        for i in range(1, 255):  # Doorloop alle mogelijke hosts in het subnet
            target_ip = f"{subnet}.{i}"
            try:
                # Probeer verbinding te maken om te zien of de host actief is
                socket.create_connection((target_ip, 80), timeout=0.5)
                active_hosts.append(target_ip)
            except (socket.timeout, OSError):
                pass  # Als de host niet reageert, negeer dan de fout

        print(f"Gevonden actieve hosts: {active_hosts}")

        # Sla resultaten op in een tekstbestand
        results_path = f"data/{hostname}/nmap_results.txt"
        os.makedirs(os.path.dirname(results_path), exist_ok=True)
        with open(results_path, "w") as results_file:
            for host in active_hosts:
                results_file.write(f"{host}\n")

        print(f"Resultaten opgeslagen in: {results_path}")

        # Retourneer de resultaten voor upload
        return {"status": "success", "active_hosts": active_hosts}

    except Exception as e:
        print(f"Fout tijdens netwerkverkenning: {e}")
        return {"status": "error", "error_message": str(e)}
