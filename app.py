import streamlit as st
import pandas as pd
import os

# 1. KONFIGURATION
st.set_page_config(page_title="SynerG Builds", page_icon="⚡", layout="wide")

# 2. DATEN LADEN
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("hardware_data.csv", sep=",")
        df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)
        df['preis'] = pd.to_numeric(df['preis'], errors='coerce').fillna(0)
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        return None

df = load_data()

if df is None:
    st.error("Datenbank nicht gefunden.")
    st.stop()

cpus = df[df['typ'] == 'cpu']
gpus = df[df['typ'] == 'gpu']

# 3. HELFER: LOGO-SUCHER (Lokal)
def show_local_logo(model_name):
    """
    Sucht nach lokalen Dateien (intel.png, amd.png, nvidia.png).
    Funktioniert immer, solange die Dateien auf GitHub liegen.
    """
    name = str(model_name).lower()
    
    # Welches Bild suchen wir?
    filename = ""
    if "intel" in name:
        filename = "intel.png"
    elif "ryzen" in name or "radeon" in name or "amd" in name:
        filename = "amd.png"
    elif "rtx" in name or "gtx" in name or "nvidia" in name:
        filename = "nvidia.png"
    
    # Prüfen, ob Datei existiert (oder vielleicht .jpg heißt)
    if os.path.exists(filename):
        st.image(filename, width=100)
    elif os.path.exists(filename.replace(".png", ".jpg")):
        st.image(filename.replace(".png", ".jpg"), width=100)
    else:
        # Falls du das Bild noch nicht hochgeladen hast:
        st.warning(f"Bild '{filename}' fehlt!")

# 4. SETUP & ANZEIGE
with st.sidebar:
    st.header("⚙️ Setup")
    selected_cpu = st.selectbox("CPU", cpus['modell'].sort_values())
    selected_gpu = st.selectbox("GPU", gpus['modell'].sort_values())
    st.write("---")
    resolution = st.select_slider("Auflösung", options=["1080p", "1440p", "4K"], value="1440p")

st.title("⚡ SynerG Builds")
st.write("Hardware-Check v1.3 (Lokale Bilder)")
st.divider()

# Daten holen
cpu_row = cpus[cpus['modell'] == selected_cpu].iloc[0]
gpu_row = gpus[gpus['modell'] == selected_gpu].iloc[0]
target_cpu = (gpu_row['score'] / {"1080p": 0.8, "1440p": 1.0, "4K": 1.5}[resolution]) * 0.6

col1, col2 = st.columns(2)

with col1:
    st.subheader("CPU")
    show_local_logo(selected_cpu) # <-- Hier wird das lokale Bild geladen
    st.markdown(f"**{selected_cpu}**")
    st.metric("Score", f"{int(cpu_row['score'])}")
    st.link_button(f"🛒 Kaufen ({cpu_row['preis']}€)", str(cpu_row.get('link', '#')))

with col2:
    st.subheader("GPU")
    show_local_logo(selected_gpu) # <-- Hier auch
    st.markdown(f"**{selected_gpu}**")
    st.metric("Score", f"{int(gpu_row['score'])}")
    st.link_button(f"🛒 Kaufen ({gpu_row['preis']}€)", str(gpu_row.get('link', '#')))

st.divider()

# Ergebnis
if cpu_row['score'] < target_cpu * 0.9:
    st.error("⚠️ CPU Bottleneck!")
elif cpu_row['score'] > target_cpu * 2.5:
    st.warning("⚠️ GPU Bottleneck!")
else:
    st.success("✅ Perfekte Synergie!")