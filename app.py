import streamlit as st
import pandas as pd

st.set_page_config(page_title="SynerG Builds", page_icon="⚡", layout="wide")

# --- HIER SIND DIE DATEN DIREKT IM CODE (FALLBACK) ---
# Das garantiert, dass es funktioniert, egal was mit der CSV ist.
data = [
    {"typ": "cpu", "modell": "Intel Core i3-12100F", "score": 14000, "preis": 95, "link": "https://amzn.to/3S8q", "bild_url": "https://m.media-amazon.com/images/I/51KoDnSuCbL._AC_SL1000_.jpg"},
    {"typ": "cpu", "modell": "Intel Core i5-13600K", "score": 38000, "preis": 320, "link": "https://amzn.to/3S8q", "bild_url": "https://m.media-amazon.com/images/I/6125mFrzr6L._AC_SL1000_.jpg"},
    {"typ": "cpu", "modell": "AMD Ryzen 5 5600",    "score": 22000, "preis": 130, "link": "https://amzn.to/3S8q", "bild_url": "https://m.media-amazon.com/images/I/61+48002TLL._AC_SL1000_.jpg"},
    {"typ": "cpu", "modell": "AMD Ryzen 7 7800X3D", "score": 45000, "preis": 380, "link": "https://amzn.to/3S8q", "bild_url": "https://m.media-amazon.com/images/I/51msA+a+jBL._AC_SL1000_.jpg"},
    {"typ": "gpu", "modell": "NVIDIA RTX 3060",     "score": 17000, "preis": 280, "link": "https://amzn.to/3S8q", "bild_url": "https://m.media-amazon.com/images/I/71M51M81cEL._AC_SL1500_.jpg"},
    {"typ": "gpu", "modell": "NVIDIA RTX 4060 Ti",  "score": 22000, "preis": 390, "link": "https://amzn.to/3S8q", "bild_url": "https://m.media-amazon.com/images/I/71w-75L3S0L._AC_SL1500_.jpg"},
    {"typ": "gpu", "modell": "AMD Radeon RX 7600",  "score": 19000, "preis": 270, "link": "https://amzn.to/3S8q", "bild_url": "https://m.media-amazon.com/images/I/71+vL+2k6gL._AC_SL1500_.jpg"},
]

df = pd.DataFrame(data)
# -----------------------------------------------------

st.title("⚡ SynerG Builds (Test-Modus)")
st.caption("Lädt Daten direkt aus dem Code, um CSV-Fehler auszuschließen.")
st.divider()

# Setup Sidebar
with st.sidebar:
    st.header("⚙️ Setup")
    cpus = df[df['typ'] == 'cpu']
    gpus = df[df['typ'] == 'gpu']
    selected_cpu = st.selectbox("CPU", cpus['modell'])
    selected_gpu = st.selectbox("GPU", gpus['modell'])
    resolution = st.select_slider("Auflösung", options=["1080p", "1440p", "4K"], value="1440p")

# Daten holen
cpu_row = cpus[cpus['modell'] == selected_cpu].iloc[0]
gpu_row = gpus[gpus['modell'] == selected_gpu].iloc[0]

# Anzeige
col1, col2 = st.columns(2)

with col1:
    st.subheader("CPU")
    # Wir nutzen hier den sichersten Weg für Bilder
    st.image(cpu_row['bild_url'], width=200)
    st.metric("Score", cpu_row['score'])
    st.write(f"**{cpu_row['modell']}**")

with col2:
    st.subheader("GPU")
    st.image(gpu_row['bild_url'], width=200)
    st.metric("Score", gpu_row['score'])
    st.write(f"**{gpu_row['modell']}**")