import pandas as pd
import requests
from io import StringIO
from collections import Counter
import random

def lade_daten(datei=None):
    if datei:
        try:
            df = pd.read_csv(datei, sep=";", encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(datei, sep=";", encoding="latin-1")
    else:
        url = "https://lotto-datenbank.de/euro_jackpot_absteigend.csv"
        content = requests.get(url).content.decode("latin-1")
        df = pd.read_csv(StringIO(content), sep=";", encoding="latin-1")

    ziehungen = []
    for _, row in df.iterrows():
        try:
            datum = pd.to_datetime(row["Datum"], dayfirst=True)
            haupt = [int(row[f"Zahl{i}"]) for i in range(1, 6)]
            euro = [int(row[f"Euro{i}"]) for i in range(1, 3)]
            ziehungen.append({
                'datum': datum,
                'haupt': haupt,
                'euro': euro
            })
        except Exception:
            continue
    return ziehungen

def berechne_haeufigkeit(ziehungen):
    hauptzahlen_counter = Counter()
    eurozahlen_counter = Counter()

    for ziehung in ziehungen:
        hauptzahlen_counter.update(ziehung['haupt'])
        eurozahlen_counter.update(ziehung['euro'])

    return hauptzahlen_counter, eurozahlen_counter

def generiere_prognose(haupt_counter, euro_counter, modus="Gewichtet"):
    def auswahl(counter, anzahl, mix=False):
        zahlen = list(counter.keys())
        gewichte = list(counter.values())

        if mix:
            häufig = sorted(counter.items(), key=lambda x: x[1], reverse=True)[:anzahl//2]
            selten = sorted(counter.items(), key=lambda x: x[1])[:anzahl - len(häufig)]
            kombi = [z for z, _ in häufig + selten]
            return sorted(random.sample(kombi, anzahl))
        else:
            return sorted(random.choices(zahlen, weights=gewichte, k=anzahl))

    mix = modus != "Gewichtet"
    haupt = auswahl(haupt_counter, 5, mix=mix)
    euro = auswahl(euro_counter, 2)
    return {"haupt": haupt, "euro": euro}
