import streamlit as st
import pandas as pd

# 1. KONFIGURATION
st.set_page_config(page_title="SynerG Builds", page_icon="⚡", layout="wide")

# 2. DATEN LADEN
@st.cache_data
def load_data():
    try:
        # Wir laden die CSV (ganz normal, ohne Bild-Spalte)
        df = pd.read_csv("hardware_data.csv", sep=",")
        
        # Daten putzen: Zahlen erzwingen
        df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)
        df['preis'] = pd.to_numeric(df['preis'], errors='coerce').fillna(0)
        df.columns = df.columns.str.strip() # Leerzeichen aus Spaltennamen entfernen
        
        return df
    except Exception:
        return None

df = load_data()

if df is None:
    st.error("Fehler: Datenbank (hardware_data.csv) nicht gefunden oder leer.")
    st.stop()

cpus = df[df['typ'] == 'cpu']
gpus = df[df['typ'] == 'gpu']

# 3. HELFER: AUTOMATISCHE LOGOS
def get_logo_html(model_name):
    """
    Erkennt den Hersteller am Namen und gibt ein schickes Logo zurück.
    Der weiße Hintergrund (bg-white) sorgt dafür, dass man auch schwarze Logos sieht.
    """
    name = str(model_name).lower()
    logo_url = ""
    
    if "intel" in name:
        logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Intel-logo.svg/800px-Intel-logo.svg.png"
    elif "ryzen" in name or "radeon" in name or "amd" in name:
        logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/AMD_Logo.svg/800px-AMD_Logo.svg.png"
    elif "rtx" in name or "gtx" in name or "nvidia" in name:
        logo_url = "https://upload.wikimedia.org/wikipedia/de/thumb/2/21/Nvidia_logo.svg/1200px-Nvidia_logo.svg.png"
    else:
        return "<div></div>" # Kein Logo gefunden

    # Wir bauen HTML mit weißem Hintergrund, damit es immer gut aussieht
    return f"""
    <div style="background-color: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 12px; display: inline-block; margin-bottom: 10px;">
        <img src="{logo_url}" style="height: 50px; width: auto;">
    </div>
    """

# 4. SEITENLEISTE
with st.sidebar:
    st.header("⚙️ Setup")
    selected_cpu = st.selectbox("Prozessor (CPU)", cpus['modell'].sort_values())
    selected_gpu = st.selectbox("Grafikkarte (GPU)", gpus['modell'].sort_values())
    st.write("---")
    resolution = st.select_slider("Auflösung", options=["1080p", "1440p", "4K"], value="1440p")
    st.caption("v1.2 - Auto-Logos")

# 5. HAUPTBEREICH
st.title("⚡ SynerG Builds")
st.write("Checke deine Hardware auf Bottlenecks.")
st.divider()

# Ausgewählte Daten finden
try:
    cpu_row = cpus[cpus['modell'] == selected_cpu].iloc[0]
    gpu_row = gpus[gpus['modell'] == selected_gpu].iloc[0]
except IndexError:
    st.error("Datenbank-Fehler: Modell nicht gefunden.")
    st.stop()

# Berechnung
res_factor = {"1080p": 0.8, "1440p": 1.0, "4K": 1.5}
target_cpu = (gpu_row['score'] / res_factor[resolution]) * 0.6

# --- ANZEIGE ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("CPU")
    # Automatisches Logo anzeigen
    st.markdown(get_logo_html(selected_cpu), unsafe_allow_html=True)
    
    st.markdown(f"### {selected_cpu}")
    st.metric("Benchmark Score", f"{int(cpu_row['score'])}")
    st.link_button(f"🛒 Kaufen ({cpu_row['preis']}€)", str(cpu_row.get('link', '#')))

with col2:
    st.subheader("GPU")
    # Automatisches Logo anzeigen
    st.markdown(get_logo_html(selected_gpu), unsafe_allow_html=True)
    
    st.markdown(f"### {selected_gpu}")
    st.metric("Benchmark Score", f"{int(gpu_row['score'])}")
    st.link_button(f"🛒 Kaufen ({gpu_row['preis']}€)", str(gpu_row.get('link', '#')))

st.divider()

# --- ERGEBNIS ---
if cpu_row['score'] < target_cpu * 0.9:
    st.error(f"⚠️ **CPU Bottleneck!** \n\nDie {selected_cpu} bremst deine Grafikkarte in {resolution} aus.")
elif cpu_row['score'] > target_cpu * 2.5:
    st.warning(f"⚠️ **GPU Bottleneck!** \n\nDie {selected_cpu} langweilt sich. Du könntest eine viel stärkere Grafikkarte nutzen.")
else:
    st.success("✅ **Perfekte Synergie!** \n\nDie Komponenten passen hervorragend zusammen.")

st.write("---")
st.caption("Hinweis: Enthält Affiliate-Links.")