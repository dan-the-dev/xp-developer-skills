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
| `worker` | no | identificativo **anonimo** di chi ha completato l'item (`W1`, `W2`…) — serve solo per gli stream paralleli |

Date ISO 8601 (`2026-09-08T16:45:00Z` o `2026-09-08`). Cycle time = `completed_at − started_at`; lead time = `completed_at − ready_at`, con ripiego su `started_at` (marcato) se `ready_at` manca.

## Da dove prendere i dati

| Input dell'utente | Cosa fare |
|-------------------|-----------|
| Testo o tabella incollati | Estrai i campi riga per riga e costruisci il CSV. |
| File caricato (CSV, foglio di calcolo, export) | Mappa le colonne sullo schema. Se il mapping non è ovvio (più colonne di data, nomi ambigui), proponilo e chiedi conferma una volta. Un foglio di calcolo si converte in CSV prima di lanciare lo script. |
| Link a card, ticket, epic, board | Usa i connettori e i tool disponibili in sessione per leggere gli item e, se possibile, la **history dei cambi di stato** (è da lì che vengono `started_at` e `completed_at` affidabili). Se la history non è disponibile, usa le date che ci sono (es. creazione/risoluzione) e **dichiara il ripiego**. |
| Numeri a mano | Vanno bene se sono una lista di completamenti datati. Una media ("5 a settimana") non è uno storico: spiega che serve la serie. |
| Nessun dato storico | **Fermati e chiedilo** (vedi sotto). Non lanciare lo script. |

## Storico mancante: fermati e chiedi

Lo storico del team è l'unico input che rende la previsione significativa. Se l'utente non l'ha fornito (né in chat, né come file, né come link leggibile con i tool della sessione):

1. **Non lanciare lo script** e non mostrare date.
2. **Non usare sostituti:** niente dati di esempio (`tools/montecarlo/examples/`), dati sintetici, storici di altri team o throughput stimati — nemmeno come "demo" dichiarata. Una demo si fa solo se l'utente la chiede esplicitamente.
3. **Chiedi lo storico in una sola domanda**, insieme agli altri dati indispensabili mancanti (item rimanenti, ordine dei gruppi, mappatura degli stati se nota come ambigua), offrendo due modi:
   - **incollarlo in chat** (tabella o elenco: `id`, data di inizio, data di completamento; tipo/tag facoltativi);
   - **indicare il percorso di un file locale** (CSV, foglio di calcolo, export del sistema di tracking).
   Se in sessione ci sono connettori verso un sistema di tracking, cita anche la possibilità di dare un link a board/epic.
4. Spiega in una riga cosa serve: item completati con date, idealmente 8–12 settimane e ~20+ item.
5. Riprendi dal passo di raccolta quando arrivano i dati.

Rete di sicurezza nello script: se `--history` punta a `tools/montecarlo/examples/`, `montecarlo.py` esce con errore. Lo accetta solo con `--demo`, che le skill passano **solo** su richiesta esplicita di una demo; in quel caso il report è marcato `data.demo: true` e va presentato come demo, non come previsione.

Questa regola prevale sulle istruzioni generiche di "agire in autonomia": senza storico non c'è nulla da prevedere.

## Regole di normalizzazione

1. **Mappatura degli stati.** Se non è chiaro quale stato o evento significhi "iniziato" e "completato", chiedilo **una sola volta**. Non assumere mai cosa significhi "fatto". Riporta sempre nell'output la mappatura usata.
2. **Solo item foglia.** Se gli item hanno sotto-elementi (sub-task, figli), conta solo le foglie ed evita i doppi conteggi tra padre e figli. Dichiara la scelta.
3. **Esclusioni.** Escludi item annullati, archiviati o chiusi senza essere stati realizzati, salvo diversa indicazione. Dichiara cosa hai escluso e quanti.
4. **Tracciabilità.** L'output dice sempre da dove sono stati presi i dati e quanti item sono entrati nel campione.
5. **Nessuna informazione sensibile nel CSV oltre al necessario:** id, tipo, tag, date, worker anonimo. Niente titoli, descrizioni o nomi di persone.
6. **Colonna `worker`** (solo se servono stream paralleli):
   - usa l'**owner primario** dell'item (assegnatario o owner principale). Se gli owner sono più di uno, l'item va al primo;
   - **anonimizza** con una mappa costante per tutta l'esecuzione: la prima persona incontrata diventa `W1`, la seconda `W2`, e così via. La mappa resta nella sessione e non entra nel CSV né nell'output. Mai nomi, email o username;
   - gli item **senza owner** restano nel CSV con `worker` vuoto. Lo script li esclude dal campione per-worker e li conta: dichiaralo comunque nella presentazione.
7. **Dipendenze tra item rimanenti** (file `--work`): ricavale dai link del sistema di tracking. Si leggono i link di blocco, non le relazioni generiche ("relates to") né la gerarchia padre/figlio:
   - "A **blocks** B" (es. Shortcut `blocks`, Jira `blocks`) → `B.depends_on` contiene `A`;
   - "B **is blocked by** A" (es. Jira `is blocked by`, Shortcut `is blocked by`) → stessa cosa;
   - un blocco verso un item **già completato** si mette in `"done": [...]` (oppure si omette): è già soddisfatto;
   - un blocco verso un item **fuori dal gruppo e non completato** va chiesto all'utente: o lo aggiungi a `items`, o lo consideri soddisfatto e lo dichiari;
   - l'ordine di `items` è la **priorità** (ordine della board o del backlog): se non è noto, chiedilo una volta;
   - lo script rifiuta id duplicati, dipendenze verso id sconosciuti e cicli: correggi il file, non forzare.

## Come si comunica il risultato

- Sempre come **probabilità** su un intervallo ("c'è l'85% di probabilità di finire entro il …"), mai come data unica o media.
- 50/70/85/95 di default; l'85% è il livello di impegno usuale. Evidenzia la distanza tra 50% e 95%.
- "Quanti entro una data" si legge al contrario: "con l'85% di probabilità completiamo **almeno** N item".
- Campione piccolo (< ~20 item) o storico breve (< ~8 settimane): **affidabilità bassa**, dichiarata, ma il risultato si mostra.
- Una previsione vale fino alla successiva: **ri-prevedere** quando arrivano nuove informazioni.
- Con stream paralleli: mostra anche la **fine per catena** (item foglia), la **criticità** (quale catena decide la data) e l'**utilizzo** degli stream. Se gli stream restano spesso fermi in attesa di dipendenze, uno stream in più non accorcia la data: dillo.
- Fuori scope: stime in punti o ore, capacity per persona in ore/punti, Legge di Little come motore di previsione.

## Stream paralleli con dipendenze (`epic --work`)

Quando un gruppo è lavorato da più persone/flussi in parallelo e alcuni item ne bloccano altri, il throughput aggregato non basta. Le regole della modalità sono queste:

1. **Input:** il file `--work` con gli item rimanenti in ordine di priorità, `depends_on` per item e `done` per i blocchi già soddisfatti; `--streams N`.
2. **Assegnazione:** in ogni periodo ogni stream libero prende il prossimo item **pronto** (tutte le dipendenze completate) secondo l'ordine del file, e lo tiene fino alla fine.
3. **Sblocco t+1:** un item sbloccato nel periodo *t* è disponibile dal periodo *t+1*.
4. **Throughput per stream:** ogni stream pesca il throughput di **una persona/flusso** dal pool dei periodi-worker (colonna `worker`; per ogni worker con almeno 10 completamenti nella finestra, ogni periodo conta come un campione, zeri inclusi). Uno stream senza item pronti resta fermo e il throughput pescato in quel periodo va perso. Senza colonna `worker`, con più di uno stream, lo script si ferma con un errore. La divisione del throughput del team tra gli stream (`--stream-throughput team`) è un'alternativa più grossolana: va scelta esplicitamente e dichiarata.
5. **Split per item:** ogni item diventa `ceil(1 × U(min, max))` sotto-item; sblocca i dipendenti solo quando sono finiti tutti.
6. **Lettura:** percentili della fine complessiva, fine per item (in particolare le foglie, cioè le fini delle catene), criticità, utilizzo degli stream; con `--deadline`, probabilità di finire tutto e "con l'85% completiamo almeno N item".

Restano fuori scope la capacity per persona in ore/punti e la Legge di Little come motore: il numero di stream si dichiara, non si ricava dalla capacity.

## Riferimento

Daniel S. Vacanti, *When Will It Be Done? Lean-Agile Forecasting to Answer Your Customers' Most Important Question*.
