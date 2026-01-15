import streamlit as st
import pandas as pd

# 1. KONFIGURATION
st.set_page_config(page_title="SynerG Builds", page_icon="⚡", layout="wide")

# 2. DATEN LADEN & REINIGEN
@st.cache_data
def load_data():
    try:
        # Wir lesen alles als Text (dtype=str), damit keine Nullen entstehen
        df = pd.read_csv("hardware_data.csv", sep=",", dtype=str)
        
        # --- REINIGUNG ---
        # Wir entfernen alle Leerzeichen bei den Links (der wichtigste Schritt!)
        if 'bild_url' in df.columns:
            df['bild_url'] = df['bild_url'].str.strip()
        if 'link' in df.columns:
            df['link'] = df['link'].str.strip()
            
        # Zahlen wieder zu Zahlen machen
        df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)
        df['preis'] = pd.to_numeric(df['preis'], errors='coerce').fillna(0)
        
        return df
    except Exception as e:
        return None

df = load_data()

if df is None:
    st.error("Fehler beim Laden der Datenbank.")
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

# 4. HAUPTBEREICH
st.title("⚡ SynerG Builds")
st.write("Checke deine Hardware auf Bottlenecks.")
st.divider()

# Daten holen
cpu_row = cpus[cpus['modell'] == selected_cpu].iloc[0]
gpu_row = gpus[gpus['modell'] == selected_gpu].iloc[0]

# Berechnung
res_factor = {"1080p": 0.8, "1440p": 1.0, "4K": 1.5}
target_cpu = (gpu_row['score'] / res_factor[resolution]) * 0.6

# --- ANZEIGE FUNKTION ---
def show_component(col, title, row):
    with col:
        st.subheader(title)
        
        # Bild-Logik: Robust und sicher
        img_url = str(row.get('bild_url', ''))
        
        if img_url.lower().startswith('http'):
            try:
                # Wir nutzen wieder den Standard-Befehl, da die Links jetzt sauber sind
                st.image(img_url, width=250)
            except:
                st.warning("Bild konnte nicht geladen werden.")
        else:
            st.info("Kein Bild verfügbar")
            
        st.markdown(f"**{row['modell']}**")
        st.metric("Benchmark Score", f"{int(row['score'])}")
        st.link_button(f"🛒 Kaufen ({row['preis']}€)", row['link'])

# Spalten erzeugen
col1, col2 = st.columns(2)

# Komponenten anzeigen
show_component(col1, "Prozessor", cpu_row)
show_component(col2, "Grafikkarte", gpu_row)

st.divider()

# --- ERGEBNIS ---
if cpu_row['score'] < target_cpu * 0.9:
    st.error(f"⚠️ **CPU Bottleneck!** \n\nDeine CPU ist zu schwach für die {selected_gpu}.")
elif cpu_row['score'] > target_cpu * 2.5:
    st.warning("⚠️ **GPU Bottleneck!** \n\nDeine CPU ist sehr stark, aber die Grafikkarte kommt nicht hinterher.")
else:
    st.success("✅ **Perfekte Synergie!** \n\nCPU und GPU passen hervorragend zusammen.")

# Footer
st.write("---")
st.caption("Hinweis: Affiliate-Links enthalten.")