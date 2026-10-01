# ModuDeck
Computer portatile a piani modulari — concept di Samuele.

## Progetto
PC superiore con display, tastiera, touchpad ribaltabile sopra un piccolo telefono e tastierino telefonico a destra. Piani interi impilabili: drone, batterie, archiviazione, ulteriori espansioni. Attacchi posteriori per antenne, alimentazione e dati; viti laterali per il fissaggio.

**Stato: concept.** Quote provvisorie 320 × 230 mm. Nessuna elettronica, ricarica, connessione radio o compatibilità elettrica è stata validata. I modelli delle parti elettroniche sono sagome. L'assemblaggio STL contiene componenti separati e può richiedere riparazione: non è pronto per la fabbricazione.

## Aprire il 3D
- Apri `cad/modudeck.scad` in OpenSCAD.
- Premi F5 per anteprima, F6 per geometria.
- `exploded=false` mostra i piani assemblati.
- `phone_open=false` chiude il touchpad.
- Le 20 parti singole sono in `cad/parts/`.

## Generare STL e visualizzatore
Con Python 3 e OpenSCAD installati:
```
python scripts/build.py
```
Apri poi `ModuDeck-parts-3D.html`: menu di tutte le parti, rotazione e zoom. Nessuna libreria web esterna necessaria.

In GitHub: **Actions → Build 3D models → Run workflow** crea uno ZIP con sorgenti, STL, catalogo e visualizzatore. Il workflow è manuale; non è stato eseguito durante il caricamento iniziale.

## Documentazione
- [Catalogo delle parti](docs/PARTS.md)
- [Decisioni ancora da prendere](docs/DESIGN.md)
- [Lista materiali da completare](BOM.csv)
- [Diario personale](JOURNAL.md)

Concept e sorgenti iniziali sviluppati con assistenza IA. Registra nel diario soltanto lavoro e tempo personali effettivi; nessun finanziamento o completamento viene dichiarato.
