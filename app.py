import streamlit as st
import pandas as pd

# 1. KONFIGURATION
st.set_page_config(page_title="SynerG Builds", page_icon="⚡", layout="wide")

# 2. DATEN LADEN
@st.cache_data
def load_data():
    try:
        # csv laden
        df = pd.read_csv("hardware_data.csv", sep=",")
        
        # Daten bereinigen (Zahlen erzwingen)
        df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)
        df['preis'] = pd.to_numeric(df['preis'], errors='coerce').fillna(0)
        df.columns = df.columns.str.strip()
        
        return df
    except Exception:
        return None

df = load_data()

if df is None:
    st.error("Datenbank-Fehler.")
    st.stop()

cpus = df[df['typ'] == 'cpu']
gpus = df[df['typ'] == 'gpu']

# 3. SEITENLEISTE
with st.sidebar:
    st.header("⚙️ Setup")
    selected_cpu = st.selectbox("Prozessor (CPU)", cpus['modell'].sort_values())
    selected_gpu = st.selectbox("Grafikkarte (GPU)", gpus['modell'].sort_values())
    
    st.write("---")
    resolution = st.select_slider("Auflösung", options=["1080p", "1440p", "4K"], value="1440p")
    st.caption("SynerG Builds v1.1")

# 4. HAUPTBEREICH
st.title("⚡ SynerG Builds")
st.write("Checke deine Hardware auf Bottlenecks.")
st.divider()

# Daten holen
try:
    cpu_row = cpus[cpus['modell'] == selected_cpu].iloc[0]
    gpu_row = gpus[gpus['modell'] == selected_gpu].iloc[0]
except IndexError:
    st.error("Modell nicht gefunden.")
    st.stop()

# Berechnung
res_factor = {"1080p": 0.8, "1440p": 1.0, "4K": 1.5}
target_cpu = (gpu_row['score'] / res_factor[resolution]) * 0.6

# --- ANZEIGE DER KOMPONENTEN (Browser-Rendering) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Prozessor")
    # Der Trick: Wir nutzen Markdown, damit der Browser das Bild lädt
    img_link = cpu_row.get('bild_url', '')
    if img_link and str(img_link).startswith('http'):
        st.markdown(f'<img src="{img_link}" width="250" style="border-radius: 10px;">', unsafe_allow_html=True)
    else:
        st.write("🖼️ Kein Bild")
        
    st.markdown(f"**{selected_cpu}**")
    st.metric("Benchmark Score", f"{int(cpu_row['score'])}")
    st.link_button(f"🛒 Kaufen ({cpu_row['preis']}€)", cpu_row['link'])

with col2:
    st.subheader("Grafikkarte")
    img_link = gpu_row.get('bild_url', '')
    if img_link and str(img_link).startswith('http'):
        st.markdown(f'<img src="{img_link}" width="250" style="border-radius: 10px;">', unsafe_allow_html=True)
    else:
        st.write("🖼️ Kein Bild")
        
    st.markdown(f"**{selected_gpu}**")
    st.metric("Benchmark Score", f"{int(gpu_row['score'])}")
    st.link_button(f"🛒 Kaufen ({gpu_row['preis']}€)", gpu_row['link'])

st.divider()

# --- ERGEBNIS ---
if cpu_row['score'] < target_cpu * 0.9:
    st.error(f"⚠️ **CPU Bottleneck!** \n\nDeine CPU ist zu schwach für die {selected_gpu} in {resolution}.")
elif cpu_row['score'] > target_cpu * 2.5:
    st.warning("⚠️ **GPU Bottleneck!** \n\nDeine CPU ist sehr stark, aber die Grafikkarte kommt nicht hinterher.")
else:
    st.success("✅ **Perfekte Synergie!** \n\nCPU und GPU passen hervorragend zusammen.")

# Footer
st.write("---")
st.caption("Hinweis: Affiliate-Links enthalten.")