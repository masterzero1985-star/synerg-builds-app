import pandas as pd
import random
from datetime import datetime

# 1. Daten laden
try:
    df = pd.read_csv("hardware_data.csv")
    print("Daten erfolgreich geladen.")
except FileNotFoundError:
    print("Fehler: CSV nicht gefunden.")
    exit()

# 2. Simulation: Wir ändern testweise etwas
# (Später kommt hier die echte Abfrage an Amazon/Passmark rein)

print("Starte Update-Prozess...")

# Wir fügen eine Spalte 'letztes_update' hinzu oder aktualisieren sie
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
df['letztes_update'] = current_time

# Simulation: Wir lassen die Preise minimal schwanken (nur zum Testen der Automation!)
# Das zeigt dir morgen früh, dass der Roboter da war.
def fluctuate_price(price):
    change = random.uniform(0.98, 1.02) # +/- 2%
    return round(price * change, 2)

# Wende die Preisänderung auf die 'preis' Spalte an
df['preis'] = df['preis'].apply(fluctuate_price)

# 3. Speichern
df.to_csv("hardware_data.csv", index=False)
print(f"Update fertig! Preise aktualisiert und Zeitstempel gesetzt: {current_time}")