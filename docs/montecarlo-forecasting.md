# Previsioni Monte Carlo — regole comuni

Regole condivise dalle skill `montecarlo-single-item`, `montecarlo-epic`, `montecarlo-epics` e dall'agente `montecarlo-simulator`. Lo script è `tools/montecarlo/montecarlo.py`; dettagli tecnici in [`tools/montecarlo/README.md`](../tools/montecarlo/README.md).

## Principio: disaccoppiamento

Lo script non conosce nessun sistema di tracking e non fa chiamate di rete: legge solo dati normalizzati (CSV/JSON). **Recuperare e normalizzare i dati è compito della skill**, cioè di chi la esegue, partendo da qualunque input dell'utente.

## Schema normalizzato dello storico

| Campo | Obbligatorio | Significato |
|-------|--------------|-------------|
| `id` | sì | identificativo del work item |
| `completed_at` | sì | quando l'item è "fatto" secondo la definizione del team |
| `started_at` | consigliato | quando il lavoro è iniziato davvero (inizio del cycle time) |
| `ready_at` | no | quando l'item è stato impegnato / messo in coda (inizio del lead time) |
| `type` | no | es. feature, bug, chore — per filtrare il campione |
| `tags` | no | separati da `;` — per filtrare il campione |

Date ISO 8601 (`2026-09-08T16:45:00Z` o `2026-09-08`). Cycle time = `completed_at − started_at`; lead time = `completed_at − ready_at`, con ripiego su `started_at` (marcato) se `ready_at` manca.

## Da dove prendere i dati

| Input dell'utente | Cosa fare |
|-------------------|-----------|
| Testo o tabella incollati | Estrai i campi riga per riga e costruisci il CSV. |
| File caricato (CSV, foglio di calcolo, export) | Mappa le colonne sullo schema. Se il mapping non è ovvio (più colonne di data, nomi ambigui), proponilo e chiedi conferma una volta. Un foglio di calcolo si converte in CSV prima di lanciare lo script. |
| Link a card, ticket, epic, board | Usa i connettori e i tool disponibili in sessione per leggere gli item e, se possibile, la **history dei cambi di stato** (è da lì che vengono `started_at` e `completed_at` affidabili). Se la history non è disponibile, usa le date che ci sono (es. creazione/risoluzione) e **dichiara il ripiego**. |
| Numeri a mano | Vanno bene se sono una lista di completamenti datati. Una media ("5 a settimana") non è uno storico: spiega che serve la serie. |
| Nessun dato storico | Spiega cosa serve (lista di item completati con date di inizio e fine, idealmente 8–12 settimane e ~20+ item) e **non inventare numeri**. |

## Regole di normalizzazione

1. **Mappatura degli stati.** Se non è chiaro quale stato o evento significhi "iniziato" e "completato", chiedilo **una sola volta**. Non assumere mai cosa significhi "fatto". Riporta sempre nell'output la mappatura usata.
2. **Solo item foglia.** Se gli item hanno sotto-elementi (sub-task, figli), conta solo le foglie ed evita i doppi conteggi tra padre e figli. Dichiara la scelta.
3. **Esclusioni.** Escludi item annullati, archiviati o chiusi senza essere stati realizzati, salvo diversa indicazione. Dichiara cosa hai escluso e quanti.
4. **Tracciabilità.** L'output dice sempre da dove sono stati presi i dati e quanti item sono entrati nel campione.
5. **Nessuna informazione sensibile nel CSV oltre al necessario:** id, tipo, tag, date. Niente titoli, descrizioni o persone.

## Come si comunica il risultato

- Sempre come **probabilità** su un intervallo ("c'è l'85% di probabilità di finire entro il …"), mai come data unica o media.
- 50/70/85/95 di default; l'85% è il livello di impegno usuale. Evidenzia la distanza tra 50% e 95%.
- "Quanti entro una data" si legge al contrario: "con l'85% di probabilità completiamo **almeno** N item".
- Campione piccolo (< ~20 item) o storico breve (< ~8 settimane): **affidabilità bassa**, dichiarata, ma il risultato si mostra.
- Una previsione vale fino alla successiva: **ri-prevedere** quando arrivano nuove informazioni.
- Fuori scope: stime in punti o ore, capacity per persona, parallelismo, Legge di Little come motore di previsione.

## Riferimento

Daniel S. Vacanti, *When Will It Be Done? Lean-Agile Forecasting to Answer Your Customers' Most Important Question*.
