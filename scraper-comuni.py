import requests
import pandas as pd
import json

BASE_URL = "https://dati.elezioni.marche.it/static_json/"

# Carica la mappa dei comuni da comuni_map.json
with open("comuni_map.json", encoding="utf-8") as f:
    comuni_map = json.load(f)  # lista di dict [{"id": 54, "nome": "Agugliano"}, ...]

def get_json(filename):
    url = BASE_URL + filename
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

def parse_results(data, comune_id, comune_nome):
    results = []
    timestamp = data.get("timestamp")
    tot_sezioni = data.get("totSezioni", {}).get("TOT_SEZIO")

    voti_raggrup = data.get("votiRaggrup", {}).get("arrVotiRaggrup", {})
    tot_validi = data.get("votiRaggrup", {}).get("tvotival", 0)

    for raggrup in data.get("anagrRaggrup", []):
        nr = str(raggrup["nraggrupmacro"])
        voti_info = voti_raggrup.get(nr, {"voti": 0, "voti_nona": 0, "voti_solosindpres": 0})

        voti = voti_info["voti"]
        perc = (voti / tot_validi * 100) if tot_validi else 0

        results.append({
            "comune_id": comune_id,
            "comune_nome": comune_nome,
            "candidato": raggrup.get("nome2") or raggrup.get("nome"),
            "voti": voti,
            "voti_nona": voti_info["voti_nona"],
            "voti_solosindpres": voti_info["voti_solosindpres"],
            "percentuale": round(perc, 2),
            "sezioni_totali": tot_sezioni,
            "timestamp": timestamp
        })
    return results

# --- MAIN ---
all_results = []

for comune in comuni_map:
    comune_id = comune["id"]
    comune_nome = comune["nome"]
    filename = f"raggrup_0_{comune_id}.json"

    data = get_json(filename)
    if data:
        all_results.extend(parse_results(data, comune_id, comune_nome))
        print(f"✓ Raccolti dati per {comune_nome}")
    else:
        print(f"✗ Nessun dato per {comune_nome}")

# Crea il DataFrame finale
df = pd.DataFrame(all_results)

# Mostra anteprima
print(df.head())
# Salva in CSV
df.to_csv("risultati_comuni.csv", index=False, encoding="utf-8")

# Faccio la pivot
df_pivot = df.pivot_table(
    index="comune_nome",
    columns="candidato",
    values="percentuale",
    aggfunc="first"   # ogni comune-candidato appare una volta sola
).reset_index()

# Rimuoviamo il nome dell’asse delle colonne
df_pivot = df_pivot.rename_axis(None, axis=1)

print(df_pivot.head())

# Salviamo in CSV
df_pivot.to_csv("risultati_percentuali_tutti_candidati.csv", index=False, encoding="utf-8")



# Pivot di nuovo
pivot_all = df.pivot_table(
    index="comune_nome",
    columns="candidato",
    values="percentuale",
    aggfunc="first"
).reset_index()

# Aggiungiamo Vincitore e Margine solamente di Acquaroli e Ricci
def trova_vincitore_margine(row):
    perc_acquaroli = row.get("Francesco Acquaroli", 0)
    perc_ricci = row.get("Matteo Ricci", 0)
    if perc_acquaroli > perc_ricci:
        vincitore = "Francesco Acquaroli"
    else:
        vincitore = "Matteo Ricci"
    margine = perc_acquaroli - perc_ricci
    return pd.Series([vincitore, margine])

pivot_all[["Vincitore", "Margine"]] = pivot_all.apply(trova_vincitore_margine, axis=1)

# Rinominiamo colonna comune
pivot_all = pivot_all.rename(columns={"comune_nome": "Comune"})

# Salviamo per Flourish
pivot_all.to_csv("flourish_input_all.csv", index=False, encoding="utf-8")

print(pivot_all.head())

