import streamlit as st
import pandas as pd

st.set_page_config(page_title="SynerG Builds", page_icon="⚡", layout="wide")

# --- TEST-DATEN MIT WIKIMEDIA (Blockier-Sicher) ---
data = [
    {
        "typ": "cpu", 
        "modell": "Intel Core i5-13600K", 
        "score": 38000, 
        "preis": 320, 
        "link": "https://amzn.to/3S8q", 
        # Offizielles Intel Logo von Wikimedia (Public Domain)
        "bild_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Intel-logo.svg/800px-Intel-logo.svg.png"
    },
    {
        "typ": "cpu", 
        "modell": "AMD Ryzen 7 7800X3D", 
        "score": 45000, 
        "preis": 380, 
        "link": "https://amzn.to/3S8q", 
        # Offizielles AMD Logo
        "bild_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/AMD_Logo.svg/800px-AMD_Logo.svg.png"
    },
    {
        "typ": "gpu", 
        "modell": "NVIDIA RTX 4070", 
        "score": 30000, 
        "preis": 550, 
        "link": "https://amzn.to/3S8q", 
        # Nvidia Logo
        "bild_url": "https://upload.wikimedia.org/wikipedia/de/thumb/2/21/Nvidia_logo.svg/1200px-Nvidia_logo.svg.png"
    },
    {
        "typ": "gpu", 
        "modell": "AMD Radeon RX 7800 XT", 
        "score": 32000, 
        "preis": 530, 
        "link": "https://amzn.to/3S8q", 
        # Radeon Logo
        "bild_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Radeon_logo.svg/2560px-Radeon_logo.svg.png"
    }
]

df = pd.DataFrame(data)

# --- APP ---
st.title("⚡ SynerG Builds")
st.write("Test-Modus: Wir nutzen Wikipedia-Bilder, um Blockaden zu vermeiden.")
st.divider()

with st.sidebar:
    st.header("Setup")
    # Filter für CPU/GPU
    cpus = df[df['typ'] == 'cpu']
    gpus = df[df['typ'] == 'gpu']
    
    selected_cpu_name = st.selectbox("CPU", cpus['modell'])
    selected_gpu_name = st.selectbox("GPU", gpus['modell'])

# Daten der Auswahl finden
cpu_row = cpus[cpus['modell'] == selected_cpu_name].iloc[0]
gpu_row = gpus[gpus['modell'] == selected_gpu_name].iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.subheader("CPU")
    # Hier muss das Bild jetzt bleiben!
    st.image(cpu_row['bild_url'], width=200)
    st.markdown(f"**{cpu_row['modell']}**")
    st.metric("Score", cpu_row['score'])

with col2:
    st.subheader("GPU")
    # Hier auch!
    st.image(gpu_row['bild_url'], width=200)
    st.markdown(f"**{gpu_row['modell']}**")
    st.metric("Score", gpu_row['score'])

st.success("Wenn du die Logos siehst, funktioniert deine App perfekt!")