import streamlit as st
import pandas as pd

# 1. KONFIGURATION
st.set_page_config(page_title="SynerG Builds", page_icon="⚡", layout="wide") 
# TIPP: layout="wide" nutzt mehr Platz auf dem Bildschirm!

# Daten laden
@st.cache_data
def load_data():
    df = pd.read_csv("hardware_data.csv")
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Fehler: Datenbank nicht gefunden.")
    st.stop()

cpus = df[df['typ'] == 'cpu']
gpus = df[df['typ'] == 'gpu']

# 2. SEITENLEISTE
with st.sidebar:
    st.header("⚙️ Setup")
    selected_cpu = st.selectbox("Prozessor (CPU)", cpus['modell'])
    selected_gpu = st.selectbox("Grafikkarte (GPU)", gpus['modell'])
    st.write("---")
    resolution = st.select_slider("Auflösung", options=["1080p", "1440p", "4K"], value="1440p")

# 3. HAUPTBEREICH
st.title("⚡ SynerG Builds")
st.write("Checke deine Hardware auf Bottlenecks.")
st.divider()

# Daten holen
cpu_row = cpus[cpus['modell'] == selected_cpu].iloc[0]
gpu_row = gpus[gpus['modell'] == selected_gpu].iloc[0]

# Berechnung
res_factor = {"1080p": 0.8, "1440p": 1.0, "4K": 1.5}
target_cpu = (gpu_row['score'] / res_factor[resolution]) * 0.6

# --- ANZEIGE DER KOMPONENTEN ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("CPU")
    # Hier zeigen wir das Bild an (width sorgt dafür, dass es nicht riesig wird)
    st.image(cpu_row['bild_url'], width=200)
    st.markdown(f"**{selected_cpu}**")
    st.metric("Benchmark Score", cpu_row['score'])
    st.link_button(f"🛒 Kaufen ({cpu_row['preis']}€)", cpu_row['link'])

with col2:
    st.subheader("GPU")
    # Bild der GPU
    st.image(gpu_row['bild_url'], width=200)
    st.markdown(f"**{selected_gpu}**")
    st.metric("Benchmark Score", gpu_row['score'])
    st.link_button(f"🛒 Kaufen ({gpu_row['preis']}€)", gpu_row['link'])

st.divider()

# --- ERGEBNIS ---
if cpu_row['score'] < target_cpu:
    st.error(f"⚠️ CPU Bottleneck! Die CPU ist zu schwach für 4K/1440p Gaming mit dieser Karte.")
elif cpu_row['score'] > target_cpu * 2.5:
    st.warning("⚠️ GPU Bottleneck! Deine CPU langweilt sich.")
else:
    st.success("✅ Perfekte Synergie! Die Komponenten arbeiten optimal zusammen.")

# Footer
st.caption("---")
st.caption("Hinweis: Enthält Affiliate-Links.")