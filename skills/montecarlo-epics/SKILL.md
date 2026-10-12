---
name: montecarlo-epics
description: Previsione Monte Carlo per una LISTA ORDINATA di gruppi (epic, progetti, iniziative) lavorati uno dopo l'altro — "quando finisce ciascun gruppo della roadmap e quando finisce tutto?". In ogni trial campiona il throughput in modo continuo lungo tutta la sequenza e registra quando si raggiungono i conteggi cumulativi, così ogni gruppo ha la sua distribuzione di fine senza sommare percentili. Usala per due o più gruppi in sequenza; per un gruppo solo usa montecarlo-epic, per un singolo item montecarlo-single-item.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Monte Carlo — lista ordinata di gruppi

## Missione

Prevedere la data di fine di **ogni gruppo** di una sequenza e del **totale**, con probabilità. I gruppi si fanno uno dopo l'altro e gli item uno alla volta (nessun parallelismo). In ogni trial una **sola serie** di throughput attraversa tutta la lista: il gruppo 1 finisce quando il cumulato raggiunge N1, il gruppo 2 a N1+N2, e così via. **Non si sommano mai i percentili dei singoli gruppi**: i percentili non si sommano.

Script condiviso: **`<AMPD-root>/tools/montecarlo/montecarlo.py`** (modalità `epics`). Regole comuni di raccolta dati: **`<AMPD-root>/docs/montecarlo-forecasting.md`** (leggilo prima del passo 1).

**Risolvere `<AMPD-root>`:** se questa skill vive in `<dir>/ampd/skills/` → `<dir>/ampd`; altrimenti `$AMPD_ROOT`; altrimenti `~/.claude/ampd` o `~/.cursor/ampd`; altrimenti la radice del repository che contiene `skills/` e `tools/montecarlo/`.

---

## Passo 1 — Raccogliere i dati

- **Storico dei work item completati** del team/sistema che lavorerà la lista (almeno `id` e `completed_at`).
- **Lista ordinata dei gruppi**: nome e item rimanenti (numero o elenco di id) per ciascuno. **L'ordine conta**: se non è esplicito, chiedilo.

Fonti: file caricato (mappa le colonne, chiedi conferma se non è ovvio); testo/tabella incollati; link a roadmap, iniziative o epic (con i connettori/tool della sessione leggi i figli non completati di ogni gruppo e lo storico del team; dichiara i ripieghi); numeri a mano con una lista di completamenti datati. Senza storico: spiega cosa serve e non inventare numeri.

Regole: stato "iniziato"/"completato" chiesto una volta sola se ambiguo; solo item **foglia** (un item figlio di due gruppi va contato una volta sola, nel primo gruppo dell'ordine — dichiaralo); esclusi annullati/archiviati; tutto dichiarato nell'output.

**Split rate:** i gruppi più lontani sono spesso meno scomposti. Proponi un `split_rate` per gruppo (es. `"1.0-1.5"` per quelli non ancora raffinati) o un `--split-rate` globale, e spiega quando lo applichi.

## Passo 2 — Normalizzare

- Storico: CSV `id,type,tags,ready_at,started_at,completed_at` (ISO 8601, tag separati da `;`).
- Gruppi: `groups.json` nell'ordine di lavoro:

```json
{"groups": [
  {"name": "Gruppo A", "remaining": 8},
  {"name": "Gruppo B", "remaining_ids": ["X-1", "X-2", "X-3"]},
  {"name": "Gruppo C", "remaining": 10, "split_rate": "1.0-1.5"}
]}
```

In alternativa `--group "Nome:N"` ripetuto (aggiunto dopo i gruppi del file).

## Passo 3 — Lanciare lo script e presentare

```bash
python3 <AMPD-root>/tools/montecarlo/montecarlo.py epics \
  --history <history.csv> --groups <groups.json> \
  [--split-rate 1.0-1.3] [--start <YYYY-MM-DD>] [--deadline <YYYY-MM-DD>] \
  [--window-weeks 12] [--granularity day|week] [--calendar workdays] [--holidays <file>] \
  [--sampling uniform|weekday] [--seed 42] \
  --out-dir <dir> --format both
```

Leggi `<out-dir>/result.json` e rispondi **in italiano**:

1. **Per ogni gruppo**: tabella 50/70/85/95 con le date ("entro il …"), più il **totale** (= fine dell'ultimo gruppo). Evidenzia l'85% e la distanza 50%–95%, che cresce lungo la lista.
2. Con `--deadline`: probabilità di ciascun gruppo di finire entro la scadenza.
3. Ricorda che le date dei gruppi vengono dalla stessa simulazione e **non si sommano**; `result.sequence_consistent` deve essere `true`.
4. **Avviso sul campione** se `reliability.level` è `low`, mostrando comunque il risultato.
5. **Dati e assunzioni**: fonte, item nel campione, scartati/esclusi, finestra, calendario, granularità, split rate per gruppo, mappatura degli stati, ordine dei gruppi.
6. Suggerisci di **ri-prevedere** a ogni gruppo chiuso o cambio di scope: le previsioni lontane sono le meno affidabili.
