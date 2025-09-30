<!-- README.md (HTML-flavored) -->

<h1 align="center">Elezioni regionali nelle Marche del 2025</h1>

<p align="center" style="margin:0 0 16px">
  Strumenti per scaricare, elaborare e visualizzare i risultati elettorali a livello
  <strong>provinciale</strong> e <strong>comunale</strong> dalle pagine pubbliche di
  <code>dati.elezioni.marche.it</code>.
</p>

<hr/>

<h2>Contenuto della repository</h2>

<ul>
  <li><strong>scraper-province.py</strong><br/>
    Scarica e aggrega i risultati per circoscrizione/provincia (JSON <code>raggrup_&lt;id&gt;.json</code>) e genera <code>risultati_provinciali.csv</code>.
  </li>

  <li><strong>scraper-comuni.py</strong><br/>
    Scarica e aggrega i risultati per ciascun comune (JSON <code>raggrup_0_&lt;id_comune&gt;.json</code>) usando <code>comuni_map.json</code>.
    Produce:
    <ul>
      <li><code>risultati_comuni.csv</code> — formato “long” (Comune, Candidato, Percentuale, …)</li>
      <li><code>risultati_percentuali_tutti_candidati.csv</code> — pivot (righe = comuni, colonne = candidati, valori = %)</li>
      <li><code>flourish_input_all.csv</code> — dataset per Flourish con percentuali di tutti i candidati, vincitore e margine (Acquaroli − Ricci)</li>
    </ul>
  </li>

  <li><strong>dizionario.txt</strong><br/>
    Estratto HTML con le <code>&lt;option&gt;</code> che mappano ID → Comune (copiato dal sito).
  </li>

  <li><strong>dizionario-id-comune.py</strong><br/>
    Converte <code>dizionario.txt</code> in <code>comuni_map.csv</code> e <code>comuni_map.json</code> (id → nome comune).
  </li>

  <li><strong>comuni_map.json</strong><br/>
    Mapping ufficiale id → nome comune, usato dagli scraper.
  </li>

  <li><strong>elezioni-marche-affluenza.xlsx</strong><br/>
    Dataset di affluenza organizzato per provincia/comune (se disponibile).
  </li>

  <li><strong>Immagini</strong> (cartografia, mappe Flourish)<br/>
    Esportazioni delle mappe a livello comunale (affluenza e risultati).
  </li>
</ul>

<hr/>

<h2>Prerequisiti</h2>

<p style="margin-top:8px">
Per i pacchetti minimi:
</p>

<pre><code>pip install requests pandas beautifulsoup4
</code></pre>

<hr/>

<h2>Workflow</h2>

<ol>
  <li><strong>Costruzione del dizionario dei comuni</strong><br/>
    Partendo da <code>dizionario.txt</code> (HTML con le &lt;option&gt;), esegui:
    <pre><code>python dizionario-id-comune.py</code></pre>
    Verranno creati <code>comuni_map.csv</code> e <code>comuni_map.json</code>.
  </li>

  <li><strong>Scraping provinciale</strong><br/>
    <pre><code>python scraper-province.py</code></pre>
    Output: <code>risultati_provinciali.csv</code>.
  </li>

  <li><strong>Scraping comunale</strong><br/>
    <pre><code>python scraper-comuni.py</code></pre>
    Output principali:
    <ul>
      <li><code>risultati_comuni.csv</code></li>
      <li><code>risultati_percentuali_tutti_candidati.csv</code></li>
      <li><code>flourish_input_all.csv</code></li>
    </ul>
  </li>

  <li><strong>Visualizzazione</strong><br/>
    Importa <code>flourish_input_all.csv</code> in <a href="https://flourish.studio/" target="_blank">Flourish</a> per creare mappe comunali:
    <ul>
      <li>Campo <em>geografico</em>: nome del comune (allineato allo shapefile)</li>
      <li>Campo <em>colore</em>: <code>Vincitore</code> (palette duale: blu Acquaroli, rosso Ricci)</li>
      <li>Campo <em>intensità</em>: <code>Margine</code> (Acquaroli − Ricci, con segno)</li>
      <li>Tooltip: percentuali di tutti i candidati (colonne della pivot)</li>
    </ul>
  </li>
</ol>

<hr/>

<h2>Esempio di output</h2>

<h3>Estratto da <code>risultati_comuni.csv</code> (formato long)</h3>

<table>
  <thead>
    <tr>
      <th>Comune</th>
      <th>Candidato</th>
      <th>Percentuale</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Agugliano</td><td>Francesco Acquaroli</td><td>45.67</td></tr>
    <tr><td>Agugliano</td><td>Matteo Ricci</td><td>40.74</td></tr>
    <tr><td>Agugliano</td><td>Claudio Bolletta</td><td>2.35</td></tr>
    <tr><td>Agugliano</td><td>Lidia Mangani</td><td>1.20</td></tr>
    <tr><td>Agugliano</td><td>Beatrice Marinelli</td><td>0.50</td></tr>
  </tbody>
</table>

<h3>Estratto da <code>flourish_input_all.csv</code> (pivot + vincitore e margine)</h3>

<p>Righe = Comuni, colonne = candidati (percentuali), con colonne aggiuntive
<code>Vincitore</code> e <code>Margine</code> (calcolato come Acquaroli − Ricci).</p>

<table>
  <thead>
    <tr>
      <th>Comune</th>
      <th>Claudio Bolletta</th>
      <th>Beatrice Marinelli</th>
      <th>Lidia Mangani</th>
      <th>Francesco Gerardi</th>
      <th>Matteo Ricci</th>
      <th>Francesco Acquaroli</th>
      <th>Vincitore</th>
      <th>Margine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Agugliano</td><td>2.35</td><td>0.50</td><td>1.20</td><td>0.80</td>
      <td>40.74</td><td>45.67</td><td>Francesco Acquaroli</td><td>+4.93</td>
    </tr>
    <tr>
      <td>Ancona</td><td>1.15</td><td>0.40</td><td>1.00</td><td>0.70</td>
      <td>46.98</td><td>44.10</td><td>Matteo Ricci</td><td>-2.88</td>
    </tr>
  </tbody>
</table>

<p style="margin-top:8px">
Nota: i numeri riportati sopra sono a solo scopo illustrativo. Fare riferimento ai CSV generati per i valori effettivi.
</p>

<hr/>

<h2>Struttura dei dati sorgente</h2>

<ul>
  <li><code>raggrup_&lt;id&gt;.json</code> — risultati a livello di circoscrizione/provincia</li>
  <li><code>raggrup_0_&lt;id_comune&gt;.json</code> — risultati del singolo comune</li>
  <li>Per ciascun JSON:
    <ul>
      <li><code>anagrRaggrup</code> — anagrafica candidati/coalizioni</li>
      <li><code>votiRaggrup.arrVotiRaggrup</code> — voti per candidato (mappa su <code>nraggrupmacro</code>)</li>
      <li><code>votiRaggrup.tvotival</code> — totale voti validi (per calcolare le percentuali)</li>
      <li><code>totSezioni.TOT_SEZIO</code> — numero sezioni</li>
      <li><code>timestamp</code> — data/ora aggiornamento</li>
    </ul>
  </li>
</ul>

<hr/>

<h2>Note d’uso</h2>

<ul>
  <li>Gli endpoint JSON possono usare parametri “cache buster” tipo <code>?_=...</code>: non sono necessari nello scraper.</li>
  <li>Se il server applica restrizioni CORS per richieste cross-origin, l’esecuzione da script server–side (come questi) non ne risente.</li>
  <li>I nomi dei comuni in <code>comuni_map.json</code> devono corrispondere a quelli presenti nei confini geografici usati in Flourish, per un match corretto.</li>
</ul>

<hr/>

<h2>Esecuzione rapida</h2>

<pre><code># 1) Genera il mapping comuni
python dizionario-id-comune.py

# 2) Scraping province
python scraper-province.py

# 3) Scraping comuni
python scraper-comuni.py

# 4) Carica i CSV in Flourish per le mappe
#    - flouris h_input_all.csv per risultati comunali
#    - elezioni-marche-affluenza.xlsx per affluenza (se necessario)
</code></pre>

<h2>Versione interattiva dei risultati:</h2>
<ul>
<li> <a href="https://public.flourish.studio/visualisation/25370291/"> Risultati finali </a> </li>
<li> <a href="https://public.flourish.studio/visualisation/25374444/"> Affluenza finale </a> </li>
</ul>
