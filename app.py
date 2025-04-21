import streamlit as st
from utils import lade_daten, berechne_haeufigkeit, generiere_prognose
import pandas as pd

st.title("Harrys Lotto Prognose")
st.markdown("Diese App analysiert Eurojackpot-Ziehungen und erstellt eine intelligente Prognose.")

ziehungen = []

# Datenquelle wählen
quelle = st.radio("Datenquelle wählen:", ["Automatisch laden", "Eigene CSV hochladen"])

if quelle == "Automatisch laden":
    if st.button("Daten automatisch laden"):
        ziehungen = lade_daten()
elif quelle == "Eigene CSV hochladen":
    file = st.file_uploader("CSV-Datei mit Eurojackpot-Ziehungen hochladen", type=["csv"])
    if file:
        try:
            ziehungen = lade_daten(file)
            st.success("CSV-Datei erfolgreich geladen.")
        except Exception as e:
            st.error(f"Fehler beim Einlesen der Datei: {e}")

# Weiterverarbeitung nach Datenimport
if ziehungen:
    st.success("Ziehungen erfolgreich geladen!")

    # Zeitraumfilter
    st.subheader("Ziehungen eingrenzen")
    alle_daten = [z["datum"] for z in ziehungen]
    min_datum = min(alle_daten)
    max_datum = max(alle_daten)

    zeitraum = st.date_input("Zeitraum auswählen", [min_datum, max_datum])
    gefiltert = [z for z in ziehungen if zeitraum[0] <= z["datum"] <= zeitraum[1]]

    # Ziehungsanzahl-Slider
    st.subheader("Anzahl der letzten Ziehungen wählen")
    max_anzahl = len(gefiltert)
    anzahl = st.slider("Wie viele der letzten Ziehungen berücksichtigen?", min_value=5, max_value=max_anzahl, value=min(50, max_anzahl))
    gezielte_ziehungen = gefiltert[-anzahl:]

    # Prognose-Strategie wählen
    st.subheader("Prognose-Modus")
    modus = st.selectbox("Welche Strategie soll verwendet werden?", ["Gewichtet", "Häufig & Selten kombiniert"])

    # Analyse & Prognose
    haupt_counter, euro_counter = berechne_haeufigkeit(gezielte_ziehungen)

    st.subheader("Häufigste Hauptzahlen")
    st.write(haupt_counter.most_common(10))

    st.subheader("Häufigste Eurozahlen")
    st.write(euro_counter.most_common(5))

    st.subheader("Prognose")
    prognose = generiere_prognose(haupt_counter, euro_counter, modus=modus)
    st.write("**Hauptzahlen:**", prognose["haupt"])
    st.write("**Eurozahlen:**", prognose["euro"])
