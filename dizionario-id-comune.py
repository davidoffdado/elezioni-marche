from bs4 import BeautifulSoup
import pandas as pd

# Legge il file txt che contiene l'HTML delle <option>
with open("C:/Users/David/Desktop/dizionario.txt", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Estrae id e nome da ciascun <option>
rows = []
for opt in soup.find_all("option"):
    val = opt.get("value")
    name = opt.text.strip()
    if val and val != "0":  # salta "Tutti"
        rows.append({"id": int(val), "nome": name.title()})

# Crea un DataFrame e lo ordina per id
df = pd.DataFrame(rows).sort_values("id")

# Salva in CSV
df.to_csv("comuni_map.csv", index=False, encoding="utf-8")

# Salva in JSON
df.to_json("comuni_map.json", orient="records", force_ascii=False, indent=2)

print("Creati comuni_map.csv e comuni_map.json")

