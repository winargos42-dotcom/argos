---
argos_import: project_file
source_path: tmp/kolibrios/data/it_IT/docs/FARA.TXT
source_abs: F:\debug\argoss\tmp\kolibrios\data\it_IT\docs\FARA.TXT
source_ext: .txt
source_sha256: f44a24aebb18a72164b81ac425eede3c09cbe9a45f2b35a6ead823376c6b4636
text_sha256: 89370ef921e8972da46a5c4d4a847b5d4218655ced0344b96eaeb40ff468349e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:39
---

# FARA.TXT

- Source: `tmp/kolibrios/data/it_IT/docs/FARA.TXT`
- Extract: `text`
- SHA256: `f44a24aebb18a72164b81ac425eede3c09cbe9a45f2b35a6ead823376c6b4636`

## Content

PHARAOH TOMB

Lo scopo di questo gioco è quello di aprire un passaggio muovendo i
geroglifici per entrare nella stanza (8x8) successiva. È possibile
scambiare due geroglifici adiacenti se dopo tale azioni sono presente
almeno tre simboli in fila (orizzontale o verticale).
Se viene creata una tale sequenza, questa sparisce facendo spazio a dei
nuovi geroglifici, creati in modo casuale, che "cadono" dall'alto.
Ogni volta che vengono fatti sparire dei geroglifici si ricevono dei
punti calcolati dalla formula max(L+(L+1)^(N-3), 20*L*N), dove N è il
numero di geroglifici rimossi e L è il livello.
Per passare al livello al livello successivo è necessario rimuovere
alcuni geroglifici particolari, che variano da livello a livello. Nel
pannello inferiore è indicato quanti ne sono stati rimossi, e quanti
sono i rimanenti.

1o livello - 500
2o livello - 450
3o livello - 400
4o livello - 350
5o livello - 300
6o livello e superirio - 50*(L+1)


Nel 1o livello vi sono 6 tipi di geroglifici differenti, ad ogni
livello si aggiunge un nuovo tipo, ma mai più di dieci (quindi dal 5o
livello in poi saranno 10 tipi, senza considerare quelli speciali).

A partire dal 2o livello, per ogni combinazione di 4 o più
geroglifici, ed ogni volta che si passa un quarto di livello, il
giocatore riceve un geroglifico bonus da sostituire quando preferisce
con un altro geroglifico.

A partire dal 3o livello, per ogni combinazione di 5 o più
geroglifici, e per ogni volta che si completa un terzo del livello, il
giocatore ottiene una "chiave universale" in grado di risolvere
qualsiasi combinazione di geroglifici e che può essere quindi usata per
risolvere in un colpo più combinazioni.

A partire dal 4o livello, per ogni combinazione di 6 o più
geroglifici, e quando si completa mezzo livello, il giocatore ottiene
uno "space crooker", che gli permette, quando usato, di fare tre mosse
(non per forza in successione) diagonali.

Il giocatore non può salvare più di un geroglifico (1 usuale, 1 joker e
1 crooker).

Il gioco termina quando il giocatore non può effettuare movimenti che
gli permettono di eliminare geroglifici con quelli attualmente in gioco.

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
