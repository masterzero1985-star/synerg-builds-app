import streamlit as st
import pandas as pd

# 1. KONFIGURATION
st.set_page_config(page_title="SynerG Builds", page_icon="⚡", layout="wide")

# 2. DATEN LADEN (Mit Sicherheits-Check)
@st.cache_data
def load_data():
    try:
        # Wir geben sep="," an, damit Excel-Fehler vermieden werden
        df = pd.read_csv("hardware_data.csv", sep=",")
        
        # Sicherheitsnetz: Wir zwingen die Spalten dazu, Zahlen zu sein
        # Falls mal "14.000" statt "14000" drin steht, wird das korrigiert
        df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0)
        df['preis'] = pd.to_numeric(df['preis'], errors='coerce').fillna(0)
        
        # Spaltennamen bereinigen (Leerzeichen entfernen)
        df.columns = df.columns.str.strip()
        
        return df
    except Exception as e:
        return None

df = load_data()

if df is None:
    st.error("Fehler: Die Datei 'hardware_data.csv' konnte nicht geladen werden. Prüfe GitHub.")
    st.stop()

# --- DEBUG BEREICH (Nur für dich zur Kontrolle) ---
with st.expander("🔧 Admin: Datenbank prüfen (Klick zum Öffnen)"):
    st.write("Hier siehst du, was die App wirklich aus der Datei liest:")
    st.dataframe(df)
    st.write(f"Anzahl Zeilen: {len(df)}")
# --------------------------------------------------

cpus = df[df['typ'] == 'cpu']
gpus = df[df['typ'] == 'gpu']

# 3. SEITENLEISTE
with st.sidebar:
    st.header("⚙️ Setup")
    # Wir sortieren die Listen alphabetisch für bessere Übersicht
    selected_cpu = st.selectbox("Prozessor (CPU)", cpus['modell'].sort_values())
    selected_gpu = st.selectbox("Grafikkarte (GPU)", gpus['modell'].sort_values())
    
    st.write("---")
    resolution = st.select_slider("Auflösung", options=["1080p", "1440p", "4K"], value="1440p")
    
    st.write("---")
    st.caption("SynerG Builds v1.0")

# 4. HAUPTBEREICH
st.title("⚡ SynerG Builds")
st.write("Checke deine Hardware auf Bottlenecks.")
st.divider()

# Daten für die Auswahl holen
# Wir nutzen try/except, falls durch das Update mal ein Modell nicht gefunden wird
try:
    cpu_row = cpus[cpus['modell'] == selected_cpu].iloc[0]
    gpu_row = gpus[gpus['modell'] == selected_gpu].iloc[0]
except IndexError:
    st.error("Fehler: Gewähltes Modell nicht in der Datenbank gefunden.")
    st.stop()

# Berechnung
res_factor = {"1080p": 0.8, "1440p": 1.0, "4K": 1.5}
target_cpu = (gpu_row['score'] / res_factor[resolution]) * 0.6

# --- ANZEIGE DER KOMPONENTEN (Diagnose-Modus) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Prozessor")
    # Wir testen: Was steht wirklich im Link?
    st.caption(f"Debug-Link: {cpu_row.get('bild_url')}") 
    
    # Versuch 1: Das Bild anzeigen
    try:
        st.image(cpu_row['bild_url'], width=250)
    except:
        st.error("Bild konnte nicht geladen werden.")
        
    st.markdown(f"**{selected_cpu}**")
    st.metric("Benchmark Score", f"{int(cpu_row['score'])}")
    st.link_button(f"🛒 Kaufen ({cpu_row['preis']}€)", cpu_row['link'])

with col2:
    st.subheader("Grafikkarte")
    st.caption(f"Debug-Link: {gpu_row.get('bild_url')}")
    
    try:
        st.image(gpu_row['bild_url'], width=250)
    except:
        st.error("Bild konnte nicht geladen werden.")
        
    st.markdown(f"**{selected_gpu}**")
    st.metric("Benchmark Score", f"{int(gpu_row['score'])}")
    st.link_button(f"🛒 Kaufen ({gpu_row['preis']}€)", gpu_row['link'])

st.divider()

# --- ERGEBNIS ---
# Kleine Toleranzzone eingebaut (damit nicht sofort "Bottleneck" steht bei kleinen Abweichungen)
if cpu_row['score'] < target_cpu * 0.9:
    st.error(f"⚠️ **CPU Bottleneck!** \n\nDeine CPU ist zu schwach für die {selected_gpu} in {resolution}. Die Grafikkarte wird ausgebremst.")
elif cpu_row['score'] > target_cpu * 2.5:
    st.warning("⚠️ **GPU Bottleneck!** \n\nDeine CPU ist sehr stark, aber die Grafikkarte kommt nicht hinterher. Zum Zocken okay, aber du hast Geld für CPU-Leistung bezahlt, die du nicht nutzt.")
else:
    st.success("✅ **Perfekte Synergie!** \n\nCPU und GPU passen hervorragend zusammen. Kein nennenswerter Flaschenhals.")

# Footer
st.write("---")
st.caption("Hinweis: Bei den verlinkten Buttons handelt es sich um Affiliate-Links. Wenn du darüber kaufst, erhalten wir eine kleine Provision.")