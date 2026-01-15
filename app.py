import streamlit as st
import pandas as pd

# 1. KONFIGURATION
st.set_page_config(page_title="SynerG Builds", page_icon="⚡")

# Daten laden
@st.cache_data
def load_data():
    df = pd.read_csv("hardware_data.csv")
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Fehler: Die Datei 'hardware_data.csv' wurde nicht gefunden.")
    st.stop()

cpus = df[df['typ'] == 'cpu']
gpus = df[df['typ'] == 'gpu']

# 2. SEITENLEISTE
with st.sidebar:
    st.header("⚙️ Konfiguration")
    selected_cpu = st.selectbox("Prozessor (CPU)", cpus['modell'])
    selected_gpu = st.selectbox("Grafikkarte (GPU)", gpus['modell'])
    st.write("---")
    resolution = st.select_slider("Auflösung", options=["1080p", "1440p", "4K"], value="1440p")

# 3. HAUPTBEREICH
st.title("⚡ SynerG Builds")
st.write("Checke deine Hardware auf Bottlenecks.")

# Werte holen
cpu_score = cpus[cpus['modell'] == selected_cpu]['score'].values[0]
gpu_score = gpus[gpus['modell'] == selected_gpu]['score'].values[0]

# Berechnung (Vereinfachter Algorithmus)
res_factor = {"1080p": 0.8, "1440p": 1.0, "4K": 1.5}
target_cpu = (gpu_score / res_factor[resolution]) * 0.6

st.divider()

col1, col2 = st.columns(2)
col1.metric("CPU Leistung", cpu_score)
col2.metric("GPU Leistung", gpu_score)

if cpu_score < target_cpu:
    st.error(f"⚠️ CPU Bottleneck! Deine CPU bremst in {resolution}.")
elif cpu_score > target_cpu * 2.5:
    st.warning("⚠️ GPU Bottleneck (CPU ist sehr stark, Grafikkarte limitiert).")
else:
    st.success("✅ Perfekte Synergie! Passt super zusammen.")