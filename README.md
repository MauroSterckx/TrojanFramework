# TrojanFramework

Ethical hacking AP Hogeschool opdracht

## Bevindingen

### Basisstructuur

#### Modulariteit

Het framework is ontworpen om modules dynamisch te laden en uit te voeren. Het is dus mogelijk om modules of andere functionaliteiten toe te voegen zonder de hoofdcode te wijzigen.

De attacker hoeft enkel de main.py code te kunnen laten runnen op de victim zijn device. De trojan zal dan automatisch de benodigde files van github downloaden (zoals config, modules, etc), uitvoeren en dan direct na uitvoering weer verwijderen zodat kans op detectie minder is. Let op dat je wel de benodigde libraries installeert, je kan deze en de juiste versie vinden in de `requirements.txt`

Daarnaast gebruikt de trojan een willekeurig getal tussen de 20 en 120 seconden om te bepalen om de hoeveel tijd de trojan opnieuw aangeroepen wordt en opnieuw uitgevoerd zal worden. Dit heb ik gedaan om detectie te voorkomen. Dit is iets wat men in de praktijk ook vaak gebruikt.

Momentueel is het zo dat de trojan debug informatie print in de terminal, dit is gedaan om ongewenste acties te voorkomen en controle te behouden bij de operator

#### Gegevensbeheer

De resultaten van modules worden opgeslagen in een JSON-bestand in de GitHub-repository. Het correct verwerken van bestaande data zonder deze te overschrijven bleek een uitdaging.

De integratie van fouttolerantie in het schrijven en lezen van data voorkomt corruptie en verlies van informatie.

Ik heb gebruik gemaakt van hashing om te bepalen of lokale files anders waren dan files in de github repo.

Aangezien we rekening moesten houden met botnets heb ik de hostname van de victim opgevraagt doormiddel van socket, deze hostname wordt gebruikt als identifier voor een bepaald systeem. In de toekomst ben ik van plan UUID's te gebruiken.

### Modules

Hier leg ik elke module een beetje uit. Je kan ook de filmpjes die meegeleverd zijn bekijken om de werking te zien.

#### Network_scan

Deze module scant het lokale subnet van de client en verzamelt IP-adressen die actief zijn. Het juiste subnet ophalen was complex omdat standaard 127.0.0.1 (localhost) werd gebruikt. Dit werd opgelost door de actieve netwerkinterface automatisch te detecteren.

Ik heb scapy gebruikt in plaats van bijvoorbeeld socket, omdat het gebruik van scapy kracht en flexibiliteit biedt, maar vereist root-toegang (sudo), wat de uitvoerbaarheid kan beperken op bepaalde systemen.

Compatibiliteit tussen verschillende netwerkconfiguraties (bijvoorbeeld meerdere netwerkinterfaces) moest goed worden getest.

#### Reverse_shell

De module opent een TCP-reverse shell naar een vooraf gedefinieerd IP-adres en poort, die uit de GitHub-configuratie wordt geladen. Dit biedt flexibiliteit in het dynamisch instellen van het doel.

De gebruikte code is lichtgewicht en eenvoudig, waardoor het gemakkelijk integreert met de main-structuur.

Er wordt verwacht dat op de remote machine wel bijvoorbeeld een netcat reverse shell listener open staat.

#### Screenshot

De module maakt een screenshot van het scherm van de client. Met behulp van de Pillow-bibliotheek kon een platformonafhankelijke oplossing worden ontwikkeld.

Het opslaan en doorsturen van de screenshot naar GitHub werkte betrouwbaar na encoding.

Op systemen zonder een actieve grafische interface (bijvoorbeeld headless servers) werkte de module niet. Dit kan worden opgelost door een check toe te voegen voor de beschikbaarheid van een GUI.

#### webcam_capture

Deze module opent de webcam van de client en maakt een foto. OpenCV bleek een geschikte bibliotheek dankzij de eenvoudige toegang tot hardwarebronnen.

Het correct afsluiten van de webcam na het maken van de foto was essentieel om resources vrij te maken en toekomstige problemen te vermijden.

Het installeren van OpenCV (opencv-python-headless voor servers en opencv-python voor clients met GUI) vergde handmatige aanpassingen op sommige platforms.

Niet alle systemen hebben een webcam, wat zorgt voor foutmeldingen. Dit werd opgevangen door foutafhandeling .

### Ethische overwegingen

Eerst en vooral geef ik geen toestemming dat (stukken van) mijn code gebruikt wordt voor kwaadwillig gebruik. De aard van het framework maakt het gevoelig voor misbruik.

Het framework is bedoeld voor educatieve doeleinden en het trainen van cybersecurityprofessionals in gecontroleerde omgevingen. Wanneer deze intentie duidelijk is en er toestemming is van alle betrokken partijen, is het gebruik van dergelijke tools ethisch verantwoord.

De ontwikkeling van dit framework was een opdracht voor het vak Ethical Hacking op de AP Hogeschool Antwerpen. De ontwikkeling zelf biedt waardevolle educatieve mogelijkheden en helpt bij het begrijpen van de werking van malware en penetratietools.

Concreet heeft het mij zowel technische als mijn begrip voor de etische implicaties van ethical hacking verbeterd. Ik ben persoonlijk ook van plan om deze opdracht verder uit te werken als privé projectje. Mijn doelen zijn om de modules te verbeteren, gegevensoverdracht te encrypteren en een eigen C2-server te ontwikkelen dat deze trojan kan besturen (misschien vanuit meeerdere github repo's)
