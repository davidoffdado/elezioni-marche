import requests
import pandas as pd

BASE_URL = "https://dati.elezioni.marche.it/static_json/"

# mapping id -> nome circoscrizione/provincia
CIRC_MAP = {
    1: "Ancona",
    2: "Ascoli Piceno",
    3: "Fermo",
    4: "Macerata",
    5: "Pesaro e Urbino"
}

def get_json(filename):
    url = BASE_URL + filename
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def parse_results(data, circ_id):
    """Unisce anagrafica candidati con voti per una circoscrizione"""
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
            "circoscrizione_id": circ_id,
            "circoscrizione_nome": CIRC_MAP.get(circ_id, f"ID {circ_id}"),
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

for circ_id in range(1, 6):  # circoscrizioni 1–5
    filename = f"raggrup_{circ_id}.json"
    try:
        data = get_json(filename)
        all_results.extend(parse_results(data, circ_id))
        print(f"✓ Raccolti dati per circoscrizione {circ_id} ({CIRC_MAP[circ_id]})")
    except Exception as e:
        print(f"✗ Errore con circoscrizione {circ_id}: {e}")

df = pd.DataFrame(all_results)
print(df.head())

# Salva in CSV
df.to_csv("risultati_provinciali.csv", index=False)
