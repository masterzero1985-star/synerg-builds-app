import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="SynerG Builds", page_icon="⚡", layout="wide")

st.title("⚡ SynerG Builds")
st.write("Test: Lokales Bild laden (Die sicherste Methode)")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("CPU (Internet-Link)")
    # Hier lassen wir den Wikimedia-Link zum Vergleich
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Intel-logo.svg/800px-Intel-logo.svg.png", width=200)
    st.write("Wenn du das Intel-Logo siehst, geht Internet.")

with col2:
    st.subheader("GPU (Dein hochgeladenes Bild)")
    
    # Der Code prüft, ob dein Bild wirklich da ist
    if os.path.exists("gpu.jpg"):
        st.image("gpu.jpg", width=250)
        st.success("✅ Bild 'gpu.jpg' gefunden!")
    else:
        st.error("❌ Datei 'gpu.jpg' nicht gefunden. Hast du sie hochgeladen?")

st.divider()
st.info("Anleitung: Lade ein beliebiges Bild als 'gpu.jpg' in dein GitHub-Repository hoch, damit es hier rechts erscheint.")