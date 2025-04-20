import streamlit as st
from utils import lade_daten, berechne_haeufigkeit, generiere_prognose

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

# Analyse und Prognose
if ziehungen:
    st.success("Ziehungen erfolgreich geladen!")

    # --- Zusätzliche Auswahlmöglichkeiten ---
    st.subheader("Daten filtern")
    anzahl = st.slider("Wie viele Ziehungen berücksichtigen?", min_value=10, max_value=len(ziehungen), value=50)

    gefiltert = ziehungen[-anzahl:]
    haupt_counter, euro_counter = berechne_haeufigkeit(gefiltert)

    # --- Prognose-Methode ---
    st.subheader("Prognose-Modus wählen")
    modus = st.selectbox("Welche Strategie soll verwendet werden?", ["Gewichtet", "Häufig & Selten kombiniert"])

    prognose = generiere_prognose(haupt_counter, euro_counter, modus=modus)

    st.subheader("Prognose")
    st.write("**Hauptzahlen:**", prognose["haupt"])
    st.write("**Eurozahlen:**", prognose["euro"])