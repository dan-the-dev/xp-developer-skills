---
name: montecarlo-single-item
description: Previsione per UN singolo work item (card, ticket, storia, bug) — "quando sarà pronto questo item?". Usa la distribuzione storica dei cycle time (o lead time) e restituisce una Service Level Expectation con percentili 50/70/85/95, anche per un item già in corso. Non simula il throughput. Usala quando la domanda riguarda un solo item; per un gruppo/epic usa montecarlo-epic, per più gruppi in sequenza usa montecarlo-epics.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Monte Carlo — singolo work item

## Missione

Rispondere a "quando sarà pronto questo item?" con una **probabilità**, non con una data secca: "l'85% degli item di questo tipo si chiude entro X giorni". Per un singolo item **non serve la simulazione sul throughput**: si leggono i percentili della distribuzione storica dei cycle time.

Script condiviso: **`<AMPD-root>/tools/montecarlo/montecarlo.py`** (modalità `single`). Regole comuni di raccolta dati: **`<AMPD-root>/docs/montecarlo-forecasting.md`** (leggilo prima del passo 1).

**Risolvere `<AMPD-root>`:** se questa skill vive in `<dir>/ampd/skills/` → `<dir>/ampd`; altrimenti `$AMPD_ROOT`; altrimenti `~/.claude/ampd` o `~/.cursor/ampd`; altrimenti la radice del repository che contiene `skills/` e `tools/montecarlo/`.

---

## Passo 1 — Raccogliere i dati

Serve lo **storico dei work item completati** (almeno `id`, data di inizio, data di completamento). Fonti possibili, in quest'ordine di preferenza:

1. **File caricato** (CSV, foglio di calcolo, export del sistema di tracking): mappa le colonne sullo schema; se il mapping non è ovvio, proponilo e chiedi conferma una volta.
2. **Testo o tabella incollati:** estrai id, tipo, tag e date riga per riga.
3. **Link a card, ticket o board:** usa i connettori/tool disponibili in sessione per leggere gli item completati e la history dei cambi di stato. Se la history non c'è, usa le date disponibili e **dichiara il ripiego**.
4. **Nessun dato storico:** spiega cosa serve (lista di item completati con date di inizio e fine, idealmente 8–12 settimane e almeno ~20 item) e **non inventare numeri**.

Dell'item da prevedere servono: il **tipo** (per filtrare il campione, se ha senso) e, se è già in corso, **da quanti giorni** (work item age).

Regole (dettagli nel doc condiviso):

- Se non è chiaro quale stato significa "iniziato" e quale "completato", **chiedilo una sola volta** e riporta la mappatura usata. Non assumere cosa significhi "fatto".
- Conta solo item **foglia** (niente doppi conteggi tra padre e sotto-task); dichiaralo.
- Escludi item annullati/archiviati/chiusi senza essere stati realizzati, salvo diversa indicazione; dichiara cosa hai escluso.

## Passo 2 — Normalizzare

Scrivi un CSV (nella directory di lavoro o nello scratchpad, non nel repository dell'utente se non richiesto):

```csv
id,type,tags,ready_at,started_at,completed_at
```

Date ISO 8601; tag multipli separati da `;`; campi opzionali vuoti. Obbligatori solo `id` e `completed_at`, ma per questa modalità `started_at` è necessario: gli item senza inizio non entrano nel campione dei cycle time.

## Passo 3 — Lanciare lo script e presentare

```bash
python3 <AMPD-root>/tools/montecarlo/montecarlo.py single \
  --history <history.csv> --type <tipo> \
  [--elapsed-days <età dell'item>] [--metric cycle|lead] \
  [--window-weeks 12] [--calendar workdays|all] [--holidays <file>] \
  --out-dir <dir> --format both
```

- `--metric lead` se l'utente chiede il tempo dall'impegno (to do) e non dall'inizio lavori.
- `--elapsed-days`: l'item è già aperto; lo script condiziona sugli item storici durati di più e segnala se l'item ha già superato quasi tutto lo storico.
- Filtri opzionali: `--type`, `--tag`, `--window-weeks`. `--as-of` per fissare la data di riferimento.

Leggi `<out-dir>/result.json` e rispondi **in italiano** con:

1. **La SLE come probabilità**: "c'è l'85% di probabilità che si chiuda entro X giorni (entro il <data>)"; mostra 50/70/85/95 e la distanza tra 50% e 95%.
2. **Avviso sul campione** se `reliability.level` è `low` — mostra comunque il risultato.
3. **Da dove vengono i dati** e **quanti item** sono nel campione (`data.sample_size`, `data.rejected`, `data.filtered_out`).
4. **Assunzioni**: finestra, calendario (giorni lavorativi o di calendario), metrica, mappatura degli stati, esclusioni, ripieghi (`lead_time_fallback`).
5. L'istogramma testuale da `summary.md` se aiuta.

Mai presentare una media, mai una data unica, mai stime in punti o ore.
