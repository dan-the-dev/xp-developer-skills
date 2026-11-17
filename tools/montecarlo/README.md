# Monte Carlo flow forecasting

Previsioni probabilistiche basate sul flusso (Vacanti, *When Will It Be Done?*) per:

- **un singolo work item** → Service Level Expectation dai percentili storici del cycle time (`single`)
- **un gruppo** (epic, progetto, iniziativa) → "quando finisco N item" / "quanti entro una data" (`epic`)
- **un gruppo lavorato da N stream paralleli con dipendenze tra item** (A blocca B) → fine complessiva, fine per catena, criticità (`epic --work`)
- **una lista ordinata di gruppi**, fatti uno dopo l'altro → fine di ogni gruppo e del totale (`epics`)

Componenti:

| Pezzo | Path | Ruolo |
|-------|------|-------|
| Agente | [`agents/montecarlo-simulator.md`](../../agents/montecarlo-simulator.md) | sceglie la modalità e delega alla skill (non calcola) |
| Skill | [`skills/montecarlo-single-item/`](../../skills/montecarlo-single-item/SKILL.md), [`skills/montecarlo-epic/`](../../skills/montecarlo-epic/SKILL.md), [`skills/montecarlo-epics/`](../../skills/montecarlo-epics/SKILL.md) | raccolgono e normalizzano i dati, lanciano lo script, presentano il risultato |
| Regole comuni | [`docs/montecarlo-forecasting.md`](../../docs/montecarlo-forecasting.md) | schema, fonti dei dati, mappatura stati, esclusioni, come comunicare |
| Script | `tools/montecarlo/montecarlo.py` | unico motore di calcolo, condiviso dalle tre skill |

**Disaccoppiamento.** Lo script non fa chiamate di rete, non conosce nessun sistema di tracking e non usa token o segreti: legge solo CSV/JSON normalizzati. Recuperare i dati (testo incollato, file, link tramite i connettori della sessione) è compito delle skill.

## Installazione e layout

Requisiti: **Python ≥ 3.11**, solo libreria standard (nessun `pip install`).

Lo script vive in **`tools/montecarlo/`** alla radice del repository, accanto a `skills/`, `agents/` e `docs/`. Gli script di install di AMPD copiano anche `tools/` nel bundle:

```bash
./scripts/install-claude.sh      # → ~/.claude/ampd/tools/montecarlo/montecarlo.py
./scripts/install-cursor.sh      # → ~/.cursor/ampd/tools/montecarlo/montecarlo.py
```

Perché qui: le skill sono collegate una per una nelle cartelle di discovery, quindi uno script dentro una singola skill non sarebbe raggiungibile in modo stabile dalle altre due. Le skill risolvono invece `<AMPD-root>` con la stessa regola già usata dagli agenti AMPD (bundle installato `…/ampd`, poi `$AMPD_ROOT`, poi `~/.claude/ampd` / `~/.cursor/ampd`, poi la radice del repo) e lanciano sempre `<AMPD-root>/tools/montecarlo/montecarlo.py`.

```text
tools/montecarlo/
├── montecarlo.py          # CLI: single | epic | epics
├── examples/
│   ├── history.csv        # 42 item sintetici (lug–ott 2026), con colonna worker — solo test e demo
│   ├── groups.json        # 3 gruppi ordinati, uno con split rate
│   ├── work.json          # 10 item in 2 catene con dipendenze (per epic --work)
│   ├── holidays.txt       # festività, una data per riga
│   └── config.json        # opzioni di default per gli esempi (seed 42, as_of 2026-10-12)
└── tests/
    ├── test_montecarlo.py
    ├── test_streams.py    # epic --work: dipendenze, stream, pool per worker
    └── data/              # storico sintetico con worker + caso reale anonimizzato (2 catene)
```

Test:

```bash
python3 -m unittest discover -s tools/montecarlo/tests
```

## Schema dei dati

**Storico** (CSV con intestazione, oppure JSON: array di oggetti o `{"items": [...]}`):

| Campo | Obbligatorio | Note |
|-------|--------------|------|
| `id` | sì | univoco |
| `completed_at` | sì | ISO 8601; definisce il throughput |
| `started_at` | consigliato | inizio del cycle time |
| `ready_at` | no | inizio del lead time; se manca → ripiego su `started_at` con flag |
| `type` | no | filtro `--type` |
| `tags` | no | separati da `;` (in JSON anche array); filtro `--tag` |
| `worker` | no | identificativo **anonimo** di chi ha completato l'item (`W1`, `W2`…, mai nomi o email); serve a `epic --work` con più stream |

```csv
id,type,tags,ready_at,started_at,completed_at
A-101,feature,checkout,2026-09-01T09:00:00Z,2026-09-03T08:30:00Z,2026-09-08T16:45:00Z
A-102,bug,,2026-09-02T10:15:00Z,2026-09-02T14:00:00Z,2026-09-04T11:20:00Z
A-103,feature,"reporting;export",,2026-09-07T09:10:00Z,2026-09-15T17:00:00Z
```

- Le date con fuso sono convertite in UTC; quelle senza fuso sono trattate come UTC. Una data senza ora vale mezzanotte.
- Cycle time = `completed_at − started_at`; lead time = `completed_at − ready_at`. In **giorni decimali coerenti con il calendario**: con `--calendar workdays` (default) il tempo nei weekend e nelle festività non conta (A-101: lead 5,3, cycle 3,3); con `--calendar all` sono giorni di calendario (A-101: lead 7,3, cycle 5,3).
- **Record scartati** (con motivo, nel JSON, nel markdown e nel CSV di controllo): id mancante o duplicato, `completed_at` mancante o non valido, `started_at`/`ready_at` non validi, `started_at` o `ready_at` successivi a `completed_at`. Un `ready_at` successivo a `started_at` non scarta il record: il lead time ripiega su `started_at` e il record viene marcato.
- Un file inesistente, vuoto o senza le colonne obbligatorie produce `ERRORE: …` ed exit code 2.

**Gruppi** (`epics`), nell'ordine di lavoro:

```json
{"groups": [
  {"name": "Onboarding", "remaining": 8},
  {"name": "Reporting", "remaining_ids": ["R-1", "R-2", "R-3"]},
  {"name": "Export", "remaining": 10, "split_rate": "1.0-1.5"}
]}
```

In alternativa `--group "Nome:N"`, ripetibile.

**Lavoro rimanente con dipendenze** (`epic --work`, anche come `"work"` nel `--config`):

```json
{"done": ["I0"],
 "items": [
  {"id": "I1", "depends_on": ["I0"]},
  {"id": "I2", "depends_on": ["I1"]},
  {"id": "I8", "depends_on": ["I1"], "split_rate": "1.0-1.5"}
]}
```

- L'**ordine nel file è la priorità**: uno stream libero prende sempre il primo item pronto.
- `depends_on` (facoltativo): id che devono essere completati prima. Ogni id deve essere nel file oppure in `done`, cioè già completato e quindi soddisfatto. Un id sconosciuto, un id duplicato o un ciclo producono `ERRORE: …` (exit 2); per il ciclo viene mostrato il percorso (`I1 → I2 → I1`).
- `split_rate` per item (facoltativo): vince sul `--split-rate` globale, che fa da default.
- Va bene anche un array di item senza `done`.

## Metodo

- **Niente medie.** Si campiona il throughput storico vero, con reinserimento.
- **Throughput** = item completati per periodo (giorno lavorativo o settimana) da `completed_at`, **periodi a zero inclusi**. Un completamento in un giorno non lavorativo va al giorno lavorativo precedente. La finestra parte dal primo completamento nei dati, se è più recente dell'inizio della finestra (prima non si sa se c'erano dati). In granularità settimanale le settimane sono blocchi di 7 giorni che finiscono il giorno prima di `--as-of`; una settimana parziale iniziale si scarta.
- **When:** in ogni trial si estrae un throughput per periodo finché il cumulato raggiunge N; il numero di periodi è il risultato. 10.000 trial di default.
- **How many** (`--deadline`): in ogni trial si sommano i throughput estratti per i periodi disponibili fino alla scadenza (inclusa). Si legge "almeno N item con probabilità p".
- **Epics:** una sola serie di throughput per trial lungo tutta la sequenza; si registra il periodo in cui il cumulato raggiunge N1, N1+N2, … Le fini dei gruppi sono monotone per costruzione (`sequence_consistent` nel JSON). I percentili dei gruppi non si sommano mai.
- **Single:** nessuna simulazione; percentili (nearest rank) dei cycle time (o lead time con `--metric lead`). Con `--elapsed-days` i percentili si condizionano sugli item storici durati più dell'età attuale, e si segnala se ne restano meno di 5.
- **Split rate** (`--split-rate 1.2` o `1.0-1.3`, o `split_rate` per gruppo): in ogni trial N viene moltiplicato per un fattore estratto nell'intervallo e arrotondato per eccesso.
- **Campionamento** (`--sampling weekday`): un lunedì simulato usa solo i lunedì storici, come suggerito da Vacanti tra le tecniche di selezione degli input.
- **Stream paralleli** (`epic --work`, vedi sotto).
- **Affidabilità bassa** se il campione ha meno di ~20 item o meno di ~8 settimane di storico. Il risultato si mostra comunque.
- **Riproducibilità:** `--seed`. Senza seed lo script ne sceglie uno e lo riporta nel JSON, così ogni esecuzione è ripetibile.
- Fuori scope: punti, ore, capacity per persona in ore/punti, Legge di Little come motore.

### Stream paralleli con dipendenze (`epic --work`)

Per un gruppo lavorato da **N stream** (persone o flussi) che rispettano le dipendenze tra item. In ogni trial e in ogni periodo:

1. ogni stream libero prende il **prossimo item pronto** (tutte le dipendenze completate), nell'ordine del file, e lo tiene fino alla fine;
2. ogni stream pesca il **suo** throughput del periodo (vedi sotto) e lo consuma sull'item. Se lo finisce, la capacità avanzata passa al prossimo item già pronto. Se non ci sono item pronti, lo stream resta fermo e il throughput pescato va perso;
3. un item completato nel periodo *t* sblocca i dipendenti dal periodo **t+1**.

Con lo **split** (`--split-rate` globale o `split_rate` per item), ogni item diventa `ceil(1 × U(min, max))` sotto-item, estratti a ogni trial. L'item è completo, e sblocca i dipendenti, solo quando lo sono tutti i suoi sotto-item.

**Throughput per stream** (`--stream-throughput`):

- `worker` (default quando lo storico ha la colonna `worker`): ogni stream pesca il throughput di **una persona/flusso**, non del team. Il campione è il **pool dei periodi-worker**: per ogni worker con almeno `--min-worker-items` completamenti nella finestra (default 10), un valore per ogni periodo della finestra, zeri inclusi. Gli item senza worker e quelli dei worker sotto soglia escono dal campione e sono contati (JSON, markdown, CSV di controllo). `--sampling weekday` campiona solo dai periodi-worker dello stesso giorno della settimana.
- `team`: un throughput del team per periodo, diviso in parti uguali tra gli stream (il resto va a stream casuali). Va scelto esplicitamente, ed è dichiarato nelle assunzioni.
- Con `--streams` > 1, senza colonna `worker` e senza `--stream-throughput team`, lo script esce con **errore esplicito**: niente ripieghi silenziosi. Con `--streams 1` e senza colonna `worker` usa il throughput del team (dichiarato), e il risultato coincide con `epic --remaining` (stessi percentili con lo stesso seed).

**Risultato** (`result.json` → `result`):

| Chiave | Contenuto |
|--------|-----------|
| `when` | percentili della fine complessiva, `spread` (distanza tra il percentile più basso e il più alto, es. 50%→95%), `probability_by_deadline` con `--deadline` |
| `items[]` | per ogni item: `depends_on`, `leaf` (nessuno ne dipende: la fine di una catena), percentili di fine, `criticality` |
| `criticality` | % dei trial in cui l'item è l'ultimo a finire (a pari merito contano tutti): mostra quale catena domina |
| `utilization` | % media dei periodi-stream in cui si lavora (`busy_pct`), si aspetta una dipendenza (`idle_blocked_pct`: dipendenze che strozzano il parallelismo) o non resta nulla da iniziare (`idle_drained_pct`) |
| `how_many` | con `--deadline`: "con l'85% completiamo almeno N item" (item del file, dalla stessa simulazione) |

In `data.workers`: worker nel campione con i loro completamenti, periodi-worker, quota di zeri, item senza worker esclusi, worker sotto soglia. `reliability.level` usa gli stessi criteri delle altre modalità, applicati al campione per-worker.

**Perché un'estensione di `epic` e non una modalità nuova.** La domanda è la stessa ("quando finisce questo gruppo?", "quanti entro la data?") e così il formato del risultato (`when`, `how_many`), la skill (`montecarlo-epic`) e le regole di presentazione. Cambia solo il modello del lavoro rimanente: da un conteggio a un grafo di item lavorato da N stream. `--work` attiva il modello a grafo. Senza `--work` la modalità è identica a prima, output compreso, e `--streams` & co. danno errore.

## CLI

```text
python3 montecarlo.py {single|epic|epics} [opzioni]
```

| Opzione | Default | Note |
|---------|---------|------|
| `--history` | — | CSV/JSON dello storico |
| `--demo` | off | consente lo storico di `examples/`; senza, lo script lo rifiuta (exit 2). Solo per demo richieste esplicitamente: il report è marcato `data.demo: true`, affidabilità `low` |
| `--config` | — | JSON con le stesse opzioni (`window_weeks`, `as_of`, …); i path relativi partono dal file; la CLI vince |
| `--as-of` | oggi | la finestra storica finisce il giorno prima |
| `--window-weeks` | 12 | `0` = tutto lo storico |
| `--start` | `--as-of` | partenza della previsione |
| `--granularity` | `day` | `day` (giorni lavorativi) o `week` |
| `--calendar` | `workdays` | `workdays`, `all`, o lista `mon,tue,wed,thu` |
| `--holidays` | — | file (una data per riga o JSON) o lista separata da virgole |
| `--sampling` | `uniform` | `uniform` o `weekday` |
| `--type`, `--tag` | — | filtri del campione (liste separate da virgole) |
| `--trials` | 10000 | |
| `--seed` | casuale (riportato) | |
| `--percentiles` | `50,70,85,95` | |
| `--out-dir` | `montecarlo-out` | |
| `--format` | `both` | `json`, `markdown`, `both` |
| `single`: `--metric`, `--elapsed-days` | `cycle` | |
| `epic`: `--remaining` \| `--remaining-ids`, `--deadline`, `--split-rate` | | almeno uno tra rimanenti e scadenza |
| `epic`: `--work` | — | JSON del lavoro rimanente con dipendenze (alternativo a `--remaining`) |
| `epic`: `--streams` | 1 | stream paralleli (solo con `--work`) |
| `epic`: `--stream-throughput` | `worker` | `worker` (pool dei periodi-worker) o `team` (throughput del team diviso tra gli stream) |
| `epic`: `--min-worker-items` | 10 | completamenti minimi nella finestra perché un worker entri nel pool |
| `epics`: `--groups`, `--group`, `--deadline`, `--split-rate` | | |

Output in `--out-dir`:

- `result.json`: dati strutturati (parametri, dati usati e scartati, affidabilità, assunzioni, risultato)
- `summary.md`: riepilogo in italiano, con percentili come probabilità e istogramma testuale
- `control.csv`: ogni record con stato (`used` / `filtered_out` / `rejected`), motivo, date, lead e cycle time, flag di ripiego

## Esempi

I dati di `examples/` sono **sintetici**: servono ai test e alle demo richieste esplicitamente, mai come sostituto dello storico di un team. Senza `--demo` lo script li rifiuta.

```bash
cd tools/montecarlo

# Singolo item di tipo feature
python3 montecarlo.py single --config examples/config.json --demo --type feature

# Singolo item già aperto da 4 giorni lavorativi
python3 montecarlo.py single --config examples/config.json --demo --type feature --elapsed-days 4

# Un gruppo: 24 item rimanenti, partenza 12 ottobre, quanti entro il 30 novembre
python3 montecarlo.py epic --config examples/config.json --demo --remaining 24 --start 2026-10-12 --deadline 2026-11-30

# Un gruppo con dipendenze (2 catene: I1→…→I7 e I8→I9→I10, I8 dipende da I1) su 2 stream paralleli
python3 montecarlo.py epic --config examples/config.json --demo --work examples/work.json --streams 2 --deadline 2026-11-30

# Lista di gruppi con split rate globale (il gruppo Export ha il suo)
python3 montecarlo.py epics --config examples/config.json --demo --groups examples/groups.json --split-rate 1.0-1.3
```

## Come le skill ottengono i dati

Lo script riceve sempre e solo il CSV normalizzato. Le skill lo costruiscono così (regole complete in [`docs/montecarlo-forecasting.md`](../../docs/montecarlo-forecasting.md)):

- **Testo incollato:** "abbiamo chiuso A-1 il 3/9 (iniziato il 1/9), A-2 il 5/9…" → una riga CSV per item, con date ISO.
- **File** (CSV, foglio di calcolo, export): si mappano le colonne sullo schema; se il mapping non è ovvio (es. "Created", "In progress since", "Resolved"), la skill propone il mapping e chiede conferma una volta.
- **Link** a card, epic o board: la skill usa i connettori e i tool disponibili in sessione per leggere gli item e la history dei cambi di stato, ne ricava `started_at`/`completed_at`, conta solo gli item foglia, esclude gli annullati e dichiara ogni ripiego (es. "history non disponibile: uso data di creazione e di chiusura"). Per gli stream paralleli legge anche l'owner primario (anonimizzato in `W1`, `W2`… → colonna `worker`) e i link di blocco tra gli item rimanenti (`blocks` / `is blocked by` → `depends_on` in `--work`).
- **Nessuno storico:** la skill **si ferma e lo chiede** all'utente (incollato in chat o come file locale), senza lanciare lo script e senza ripiegare sui dati di `examples/`. Lo script fa da rete di sicurezza: rifiuta lo storico di esempio se manca `--demo`.

In ogni caso l'output riporta la fonte, quanti item sono entrati nel campione, la mappatura degli stati e le esclusioni.
