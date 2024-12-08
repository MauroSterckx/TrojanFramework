# TrojanFramework

Ethical hacking AP Hogeschool opdracht

## Opdracht:

- Structuur:
  - config: Voor configuratie-informatie (zoals te runnen modules en instellingen).
  - data: Voor de verzamelde resultaten van modules.
  - modules: Voor de modulecode (uitbreidbaar met nieuwe acties).
- Configuratiebestand (config.json)
  - Bestuurt je Trojan met een lijst van modules die uitgevoerd moeten worden (is leeg
    indien slapend).
  - Hou rekening met een botnet en gebruik unieke IDʼs per client.
- Data-exfiltratie:
  - Verzamelde data wordt teruggestuurd naar de data-directory in het repository
