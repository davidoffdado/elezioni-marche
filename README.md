Elezioni Regionali Marche 2025 – Scraper e Analisi

Questo repository contiene strumenti per scaricare, elaborare e visualizzare i dati delle elezioni regionali 2025 nelle Marche, a livello provinciale e comunale.
I dati provengono dal portale ufficiale della Regione Marche (dati.elezioni.marche.it
) e sono rilasciati come open data.

Contenuto della repository

scraper-province.py
Script per raccogliere i risultati a livello provinciale (circoscrizioni).
Estrae i dati dai file JSON raggrup_<id>.json e produce risultati_provinciali.csv.

scraper-comuni.py
Script per raccogliere i risultati a livello comunale.
Usa come input il file comuni_map.json per associare l’ID di ciascun comune al relativo nome e genera risultati_comuni.csv.

dizionario.txt
Estratto HTML dal sito ufficiale con le <option> che mappano ID → Comune.
È stato usato per costruire il dizionario di associazione.

dizionario-id-comune.py
Script che legge dizionario.txt ed esporta il mapping tra ID e comune sia in formato CSV che JSON (comuni_map.csv e comuni_map.json).

comuni_map.json
Dizionario in formato JSON che associa ogni ID al nome del comune, usato come riferimento dallo scraper.

risultati_provinciali.csv
Risultati raccolti e aggregati per provincia (una riga per candidato, per provincia).

risultati_comuni.csv
Risultati raccolti e aggregati per comune (una riga per candidato, per comune).

risultati_percentuali_tutti_candidati.csv
Tabella pivotata con i comuni come righe e tutti i candidati come colonne, contenente le percentuali.

flourish_input_all.csv
File pronto per l’importazione in Flourish, con vincitore e margine calcolati per ogni comune, oltre alle percentuali per ciascun candidato.

elezioni-marche-affluenza.xlsx
File Excel con i dati di affluenza, raccolti e organizzati per provincia e comune.

Immagini della mappa
Screenshot o esportazioni da Flourish con la visualizzazione dei risultati e dell’affluenza a livello comunale.

Workflow

Creazione del dizionario dei comuni

Si parte da dizionario.txt (estratto HTML).

Lo script dizionario-id-comune.py genera comuni_map.json.

Scraping dei dati

scraper-province.py raccoglie i dati per circoscrizione (province).

scraper-comuni.py raccoglie i dati per comune, basandosi su comuni_map.json.

Elaborazione e trasformazioni

Creazione di tabelle pivot con percentuali di voto per ogni candidato.

Calcolo dei vincitori e dei margini di scarto (sia assoluti che specifici Acquaroli–Ricci).

Esportazione in formato CSV per uso diretto in Flourish.

Visualizzazione

I file CSV (flourish_input_all.csv e derivati) sono stati caricati su Flourish per generare mappe interattive, colorando i comuni in base al vincitore e all’intensità del margine.

Nel repository sono incluse alcune immagini di output ottenute con Flourish:

<img width="1135" height="1292" alt="risultati-finali" src="https://github.com/user-attachments/assets/65e0ae7d-6da2-4079-a76b-008429ff8401" />
<img width="794" height="955" alt="comuni-all" src="https://github.com/user-attachments/assets/224a9b60-aa59-40c5-b38a-55646884fa99" />

I link alla versione interattiva sono i seguenti:
https://public.flourish.studio/visualisation/25370291/
https://public.flourish.studio/visualisation/25374444/
