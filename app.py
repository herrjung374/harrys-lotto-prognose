import streamlit as st
from utils import lade_daten, berechne_haeufigkeit, generiere_prognose

st.title("Harrys Lotto Prognose")
st.markdown("Diese App analysiert Eurojackpot-Ziehungen und erstellt eine intelligente Prognose.")

# Datenquelle wählen
quelle = st.radio("Datenquelle wählen:", ["Automatisch laden", "Eigene CSV hochladen"])

if quelle == "Automatisch laden":
    ziehungen = lade_daten()
else:
    file = st.file_uploader("CSV-Datei mit Eurojackpot-Ziehungen hochladen", type=["csv"])
    if file:
        ziehungen = lade_daten(file)

if ziehungen:
    haupt_counter, euro_counter = berechne_haeufigkeit(ziehungen)

    st.subheader("Häufigste Hauptzahlen")
    st.write(haupt_counter.most_common(10))

    st.subheader("Häufigste Eurozahlen")
    st.write(euro_counter.most_common(5))

    st.subheader("Prognose")
    prognose = generiere_prognose(haupt_counter, euro_counter)
    st.write("**Hauptzahlen:**", prognose['haupt'])
    st.write("**Eurozahlen:**", prognose['euro'])
