---
name: montecarlo-epic
description: Previsione Monte Carlo per UN gruppo di work item (epic, progetto, iniziativa, release) — "quando finiamo questi N item?" e, opzionalmente, "quanti item completiamo entro una scadenza?". Campiona il throughput storico (periodi a zero inclusi) per 10.000+ trial e restituisce date con probabilità 50/70/85/95. Copre anche il gruppo lavorato da N stream paralleli con dipendenze tra item (A blocca B): fine complessiva, fine per catena e criticità. Usala per un solo gruppo; per un solo item usa montecarlo-single-item, per più gruppi in sequenza usa montecarlo-epics.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Monte Carlo — un gruppo (epic)

## Missione

Rispondere a "quando finiamo questo gruppo?" con una **distribuzione di date** riassunta in percentili, comunicata come probabilità ("c'è l'85% di probabilità di finire entro il …"). Niente medie: si campiona il throughput storico reale, periodo per periodo, finché si raggiungono gli item rimanenti.

Script condiviso: **`<AMPD-root>/tools/montecarlo/montecarlo.py`** (modalità `epic`). Regole comuni di raccolta dati: **`<AMPD-root>/docs/montecarlo-forecasting.md`** (leggilo prima del passo 1).

**Risolvere `<AMPD-root>`:** se questa skill vive in `<dir>/ampd/skills/` → `<dir>/ampd`; altrimenti `$AMPD_ROOT`; altrimenti `~/.claude/ampd` o `~/.cursor/ampd`; altrimenti la radice del repository che contiene `skills/` e `tools/montecarlo/`.

---

## Passo 1 — Raccogliere i dati

Servono due cose:

- **Storico dei work item completati** del team/sistema che lavorerà il gruppo: almeno `id` e data di completamento (il throughput usa solo `completed_at`).
- **Lavoro rimanente:** il numero di item non ancora completati nel gruppo, oppure il loro elenco di id.

Fonti possibili:

1. **File caricato** (CSV, foglio di calcolo, export): mappa le colonne sullo schema, chiedi conferma se il mapping non è ovvio.
2. **Testo o tabella incollati:** estrai i campi.
3. **Link al gruppo/epic o alla board:** con i connettori/tool della sessione leggi i figli del gruppo (rimanenti = non completati, non annullati) e lo storico degli item completati dal team. Se manca la history degli stati, usa le date disponibili e dichiara il ripiego.
4. **Solo numeri a mano** ("restano 24 item, negli ultimi 3 mesi abbiamo chiuso questi item…"): va bene se c'è una lista di completamenti datati. Un throughput medio ("facciamo 5 item a settimana") **non basta**: spiega che serve la serie storica e non inventarla.
5. **Nessuno storico fornito:** **fermati e chiedilo** — da incollare in chat o come percorso di un file locale — insieme agli altri dati mancanti, in una sola domanda. Non lanciare lo script, non usare i dati di `tools/montecarlo/examples/` né altri sostituti, neanche come demo. Solo se l'utente chiede esplicitamente una demo: aggiungi `--demo` (senza, lo script rifiuta lo storico di esempio) e presenta il risultato come demo, non come previsione. Dettagli in `docs/montecarlo-forecasting.md` § *Storico mancante*.

Regole: stato "iniziato"/"completato" chiesto una volta sola se ambiguo; solo item **foglia**; esclusi annullati/archiviati; tutto dichiarato nell'output.

**Stream paralleli e dipendenze:** se l'utente dice che il gruppo è lavorato da più persone/flussi in parallelo ("siamo in 2", "due stream"), o che alcuni item ne bloccano altri:

- leggi i **link di blocco** tra gli item rimanenti (con i tool della sessione, oppure dal testo o dal file dell'utente) e costruisci il file `--work`: item in **ordine di priorità** (board/backlog), `depends_on` da "blocks" / "is blocked by", i blocchi già completati in `"done"`. Le regole sono in `docs/montecarlo-forecasting.md` § *Regole di normalizzazione* (punto 7);
- chiedi il **numero di stream** se non è detto;
- nello storico aggiungi la colonna **`worker`**: owner primario **anonimizzato** (`W1`, `W2`…, mai nomi), il primo owner se sono più di uno, vuoto se manca. Se lo storico non ha owner, dillo: con più di uno stream lo script si ferma. Proponi due strade: recuperare gli owner, oppure `--stream-throughput team` (throughput del team diviso tra gli stream, più grossolano), da dichiarare;
- un blocco verso un item fuori dal gruppo e non completato va chiesto (aggiungerlo a `items` o considerarlo soddisfatto).

**Split rate:** se il gruppo contiene lavoro non ancora scomposto (item grandi che diventeranno più item), proponi `--split-rate` (es. `1.0-1.5`) e spiega perché.

## Passo 2 — Normalizzare

CSV `id,type,tags,ready_at,started_at,completed_at[,worker]` (date ISO 8601, tag separati da `;`, `worker` anonimo). Per il rimanente: un numero (`--remaining`), una lista di id (`--remaining-ids A-1,A-2,...`) oppure, con dipendenze o stream paralleli, il file `work.json`:

```json
{"done": ["X-0"], "items": [
  {"id": "X-1", "depends_on": ["X-0"]},
  {"id": "X-2", "depends_on": ["X-1"]},
  {"id": "X-8", "depends_on": ["X-1"], "split_rate": "1.0-1.5"}
]}
```

## Passo 3 — Lanciare lo script e presentare

```bash
python3 <AMPD-root>/tools/montecarlo/montecarlo.py epic \
  --history <history.csv> --remaining <N> \
  [--start <YYYY-MM-DD>] [--deadline <YYYY-MM-DD>] [--split-rate 1.0-1.3] \
  [--window-weeks 12] [--granularity day|week] [--calendar workdays] [--holidays <file>] \
  [--sampling uniform|weekday] [--type ...] [--tag ...] [--seed 42] \
  --out-dir <dir> --format both
```

Con stream paralleli e dipendenze:

```bash
python3 <AMPD-root>/tools/montecarlo/montecarlo.py epic \
  --history <history.csv con worker> --work <work.json> --streams 2 \
  [--deadline <YYYY-MM-DD>] [--split-rate 1.0-1.3] [--min-worker-items 10] \
  [--stream-throughput worker|team] [--sampling uniform|weekday] [--seed 42] \
  --out-dir <dir> --format both
```

- `--deadline`: aggiunge la simulazione "quanti entro la scadenza" e la probabilità di finire tutto entro quella data.
- `--sampling weekday`: un lunedì simulato campiona dai lunedì storici (utile se il throughput dipende dal giorno).
- `--seed` per risultati ripetibili.

Leggi `<out-dir>/result.json` e rispondi **in italiano**:

1. **Le date come probabilità**: tabella 50/70/85/95 ("entro il …"); evidenzia l'85% come livello di impegno e la **distanza tra 50% e 95%**.
2. Con scadenza: "c'è il X% di probabilità di finire entro <scadenza>" e "con l'85% di probabilità completiamo **almeno** N item" (lettura "N o più").
3. **Avviso sul campione** se `reliability.level` è `low` — il risultato si mostra comunque.
4. **Dati**: fonte, item nel campione, scartati/esclusi, throughput (periodi, periodi a zero).
5. **Assunzioni**: finestra, calendario e festività, granularità, split rate, mappatura degli stati, esclusioni.
6. **Con `--work`** mostra anche:
   - la **fine per catena**: i percentili degli item foglia (`result.items[]` con `leaf: true`);
   - la **criticità** (`result.criticality`): quale catena è l'ultima a finire e in che quota dei trial;
   - l'**utilizzo degli stream** (`result.utilization`): se `idle_blocked_pct` è alto, le dipendenze strozzano il parallelismo e uno stream in più non accorcia la data;
   - i **dati per worker** (`data.workers`): worker nel campione, periodi-worker, quota di zeri, item senza worker esclusi, worker sotto soglia;
   - le assunzioni specifiche: numero di stream, regola di sblocco t+1, priorità per ordine del file, split, origine del throughput per stream.
7. Suggerisci di **ri-prevedere** quando arrivano nuove informazioni (nuovi completamenti, cambi di scope).

Mai sommare medie, mai una data unica, niente punti/ore/capacity per persona: il numero di stream si dichiara, non si ricava dalla capacity.
