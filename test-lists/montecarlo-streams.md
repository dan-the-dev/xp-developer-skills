# Test list — Monte Carlo: N stream paralleli con dipendenze (`epic --work`)

## Input `--work`
- [x] id duplicato → `InputError`
- [x] dipendenza verso id inesistente → `InputError`
- [x] ciclo (anche auto-dipendenza) → `InputError` con il percorso del ciclo
- [x] dipendenza verso un id elencato in `done` è soddisfatta
- [x] `split_rate` per item vince sul `--split-rate` globale, che fa da default
- [x] `--work` e `--remaining` insieme → `InputError`

## Simulazione a stream
- [x] 2 stream, throughput 1: una catena di 3 item finisce al periodo 3
- [x] 2 stream, throughput 1: due catene indipendenti da 3 finiscono al periodo 3
- [x] 2 stream, throughput 1: B dipende dal primo item di A → B parte al periodo t+1
- [x] catena unica: 2 stream non sono più veloci di 1; l'utilizzo mostra lo stream fermo
- [x] lo split per item ritarda i dipendenti
- [x] criticità: quota di trial in cui l'item è l'ultimo a finire

## Throughput per worker
- [x] pool dei periodi-worker: un campione per periodo per worker idoneo, zeri inclusi
- [x] worker sotto `--min-worker-items` esclusi e riportati
- [x] item senza worker esclusi dal campione e contati
- [x] `--sampling weekday` campiona dai periodi-worker dello stesso giorno
- [x] `--streams 2` senza colonna `worker` → errore esplicito
- [x] `--stream-throughput team` divide il throughput del team tra gli stream

## End-to-end
- [x] 1 stream, nessuna dipendenza/split, history senza worker → stessi percentili di `epic --remaining`
- [x] 1 stream, history con un solo worker → stessi percentili di `epic --remaining`
- [x] `epic --remaining` invariato (JSON e markdown)
- [x] caso reale (2 catene, 2 stream): criticità I7 > I10, percentili per item, utilizzo, dati worker
- [x] `--deadline`: probabilità di finire tutto e "almeno N item" all'85%
- [x] esempio del README con `--demo` gira
