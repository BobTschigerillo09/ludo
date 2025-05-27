import random

# Konstanten
FARBEN = ["Rot", "Blau", "Grün", "Gelb"]
FIGUREN_PRO_SPIELER = 4
FELDER_GESAMT = 40
STARTFELD = -1
STARTPOSITIONEN = {
    "Rot": 0,
    "Blau": 10,
    "Grün": 20,
    "Gelb": 30
}
ZIELFELDER = {
    "Rot": ["RZ1", "RZ2", "RZ3", "RZ4"],
    "Blau": ["BZ1", "BZ2", "BZ3", "BZ4"],
    "Grün": ["GZ1", "GZ2", "GZ3", "GZ4"],
    "Gelb": ["YZ1", "YZ2", "YZ3", "YZ4"]
}

# Spieler anlegen
def spieler_erstellen():
    spieler_anzahl = 0
    while spieler_anzahl < 2 or spieler_anzahl > 4:
        spieler_anzahl = int(input("Wie viele Spieler spielen mit? (2-4): "))
    
    spieler_liste = []
    for i in range(spieler_anzahl):
        name = input(f"Gib den Namen von Spieler {i+1} ein: ")
        farbe = FARBEN[i]
        figuren = []
        for j in range(FIGUREN_PRO_SPIELER):
            figur = {
                "position": STARTFELD,
                "schritte": 0
            }
            figuren.append(figur)
        spieler = {
            "name": name,
            "farbe": farbe,
            "figuren": figuren
        }
        spieler_liste.append(spieler)
        print(f"{name} spielt mit {farbe}.")
    return spieler_liste

# Ausgabe aller Figurenpositionen
def spielfeld_anzeigen(spieler_liste):
    print("\nAktueller Spielstand:")
    for spieler in spieler_liste:
        print(f"{spieler['name']} ({spieler['farbe']}):")
        for i, figur in enumerate(spieler["figuren"]):
            pos = figur["position"]
            if pos == STARTFELD:
                status = "im Haus"
            elif isinstance(pos, str) and pos.endswith("Z" + str(i+1)):
                status = f"im Zielfeld ({pos})"
            else:
                status = f"auf Feld {pos}"
            print(f"  Figur {i+1}: {status} | Schritte: {figur['schritte']}")
    print()

# Figur auswählen
def figur_auswaehlen(spieler, wurf):
    moeglich = []
    for i, figur in enumerate(spieler["figuren"]):
        if figur["position"] == STARTFELD and wurf == 6:
            moeglich.append(i)
        elif isinstance(figur["position"], int) and figur["position"] >= 0:
            moeglich.append(i)

    if not moeglich:
        print("Keine Figur kann gezogen werden.")
        return None

    print("Welche Figur willst du ziehen?")
    for i in moeglich:
        pos = spieler["figuren"][i]["position"]
        print(f"{i+1}. Figur {i+1} (Position: {pos})")

    auswahl = 0
    while auswahl-1 not in moeglich:
        auswahl = int(input("Nummer der Figur: "))
    return auswahl - 1

# Figur bewegen
def figur_bewegen(spieler, figur_index, wurf, alle_spieler):
    figur = spieler["figuren"][figur_index]

    if figur["position"] == STARTFELD:
        start_pos = STARTPOSITIONEN[spieler["farbe"]]
        figur["position"] = start_pos
        figur["schritte"] = 1
        print(f"Figur kommt ins Spiel auf Feld {start_pos}!")
    else:
        figur["schritte"] += wurf
        zielbereich = ZIELFELDER[spieler["farbe"]]

        if figur["schritte"] > FELDER_GESAMT:
            ziel_index = figur["schritte"] - FELDER_GESAMT - 1
            if ziel_index < len(zielbereich):
                figur["position"] = zielbereich[ziel_index]
                print(f"Figur ist im Zielfeld: {figur['position']}")
            else:
                print("Zug ungültig – Figur kann nicht weiter, Ziel voll.")
                figur["schritte"] -= wurf
                return
        else:
            neue_position = (figur["position"] + wurf) % FELDER_GESAMT
            figur["position"] = neue_position
            print(f"Figur zieht auf Feld {neue_position}")

            # Prüfen ob andere Figur geschlagen wird
            for anderer_spieler in alle_spieler:
                if anderer_spieler["name"] != spieler["name"]:
                    for andere_figur in anderer_spieler["figuren"]:
                        if andere_figur["position"] == figur["position"]:
                            if isinstance(andere_figur["position"], int):
                                andere_figur["position"] = STARTFELD
                                andere_figur["schritte"] = 0
                                print(f"{spieler['name']} hat eine Figur von {anderer_spieler['name']} geschlagen!")

# Gewinnbedingung prüfen
def hat_gewonnen(spieler):
    for figur in spieler["figuren"]:
        if not isinstance(figur["position"], str) or not figur["position"].startswith(spieler["farbe"][0]):
            return False
    return True

# Spiel starten
def spiel_starten():
    spieler = spieler_erstellen()
    aktuelle_reihe = 0
    gewonnen = False

    while not gewonnen:
        aktueller_spieler = spieler[aktuelle_reihe]
        print(f"\n--- {aktueller_spieler['name']} ({aktueller_spieler['farbe']}) ist am Zug ---")
        input(f"{aktueller_spieler['name']}, drücke Enter zum Würfeln...")
        wurf = random.randint(1, 6)
        print(f"{aktueller_spieler['name']} würfelt eine {wurf}")

        index = figur_auswaehlen(aktueller_spieler, wurf)
        if index is not None:
            figur_bewegen(aktueller_spieler, index, wurf, spieler)

        spielfeld_anzeigen(spieler)

        if hat_gewonnen(aktueller_spieler):
            print(f"🎉 {aktueller_spieler['name']} ({aktueller_spieler['farbe']}) hat gewonnen! 🎉")
            gewonnen = True
        else:
            if wurf != 6:
                aktuelle_reihe = (aktuelle_reihe + 1) % len(spieler)

# Hauptprogramm starten
spiel_starten()




 












