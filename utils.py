import pandas as pd
from collections import Counter
import random
import requests
from io import StringIO

def lade_daten(datei=None):
    if datei:
        df = pd.read_csv(datei, sep=";")
    else:
        url = "https://www.lottozahlenonline.de/eurojackpot/gewinnzahlen.csv"
        try:
            content = requests.get(url).content.decode("utf-8")
            df = pd.read_csv(StringIO(content), sep=";")
        except:
            return []

    ziehungen = [datum]
    for _, row in df.iterrows():
        try:
            haupt = [int(row[f"Zahl{i}"]) for i in range(1, 6)]
            euro = [int(row[f"Euro{i}"]) for i in range(1, 3)]
            ziehungen.append({'haupt': haupt, 'euro': euro})
        except:
            continue
    return ziehungen

def berechne_haeufigkeit(ziehungen):
    hauptzahlen_counter = Counter()
    eurozahlen_counter = Counter()

    for ziehung in ziehungen:
        hauptzahlen_counter.update(ziehung['haupt'])
        eurozahlen_counter.update(ziehung['euro'])

    return hauptzahlen_counter, eurozahlen_counter

def generiere_prognose(haupt_counter, euro_counter):
    def gewichtet_auswahl(counter, anzahl, mix=False):
        zahlen = list(counter.keys())
        werte = list(counter.values())

        if mix:
            häufig = sorted(counter.items(), key=lambda x: x[1], reverse=True)[:anzahl//2]
            selten = sorted(counter.items(), key=lambda x: x[1])[:anzahl - len(häufig)]
            kombi = [z for z, _ in häufig + selten]
            return sorted(random.sample(kombi, anzahl))
        else:
            return sorted(random.choices(zahlen, weights=werte, k=anzahl))

    haupt = gewichtet_auswahl(haupt_counter, 5, mix=True)
    euro = gewichtet_auswahl(euro_counter, 2)
    return {"haupt": haupt, "euro": euro}
