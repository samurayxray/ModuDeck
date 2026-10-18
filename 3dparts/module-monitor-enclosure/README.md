# Module Monitor — riferimenti per il contenitore preliminare

Verifica tecnica assistita da Codex, 18 ottobre 2026. Questo testo descrive file e controlli, non è un diario personale. Non sono state attribuite ore.

**Stato: CAD preliminare assistito.** Dopo l'analisi dei riferimenti, il proprietario ha richiesto la modellazione automatica: [DWG, STL, controlli e catture v02](preliminary/assisted-v02/README.md). Esiste un'interferenza PCB/torretta da correggere. Il proprietario dispone soltanto del PC; non sono disponibili componenti fisici per prove di accoppiamento. Le sezioni seguenti conservano l'analisi dei riferimenti elettronici precedente al contenitore; i risultati attuali del contenitore sono descritti nella revisione v02.

## File effettivamente disponibili

- [PCB canonica](../../electronics/module-monitor/ModuDeck-Module-Monitor.kicad_pcb) e [progetto KiCad](../../electronics/module-monitor/ModuDeck-Module-Monitor.kicad_pro). I KiCad nella radice sono una revisione precedente.
- [Assieme STEP esportato da KiCad](reference/module-monitor-pcb-assembly.step), in millimetri, con 17 istanze dei modelli 3D disponibili. È un riferimento elettronico, non un pezzo da stampare.
- [Contorno, fori, piazzole e trasformazioni dei modelli](reference/pcb-geometry.json), [posizioni componenti CSV](reference/component-positions.csv) e [comando/log dell'esportazione](reference/step-export.json).
- STEP di dettaglio: [substrato PCB](reference/pcb-body.step), [Pico e zoccoli](reference/pico-and-sockets.step), [morsetto J1](reference/terminal-j1.step).
- [Verifica geometrica STEP](checks/step-geometry.json), [inventario del visualizzatore esistente](checks/existing-viewer-inventory.json) e [tracciabilità](checks/provenance.json).
- [Guida alla modellazione personale](MODELLAZIONE-GUIDATA.md). Il futuro DWG e gli STL preliminari andranno in [preliminary/](preliminary/README.md).

I modelli OpenSCAD in `cad/` riguardano il computer completo e vassoi. Lo studio `cad/thinkpad-study/` e il visualizzatore locale `E:/moduldeck/ModuDeck-ThinkPad-3D.html` contengono 18 parti preliminari del computer. Non sono il contenitore del Module Monitor. Il visualizzatore contiene mesh, non un DWG o una prova di accoppiamento. I blueprint e le illustrazioni locali esaminati descrivono concept; le tavole `2.png`–`11.png`, `123.png` e `321.png` dichiarano esplicitamente l'origine AI. Non vengono usati per ricavare quote o come screenshot CAD.

## Quote ricavate dal file PCB

Coordinate sul lato componenti: origine all'angolo superiore sinistro del contorno, X a destra, Y verso il basso. Il contorno assoluto KiCad va da (100,50) a (190,120) mm.

| Elemento | Dato dal file |
| --- | --- |
| Contorno | Rettangolo 90 × 70 mm, quattro segmenti chiusi |
| Spessore nominale | 1,6 mm |
| H1, H2 | (5,5), (85,5) mm |
| H3, H4 | (5,65), (85,65) mm |
| Fori di montaggio | Quattro Ø3,2 mm NPTH; interassi 80 × 60 mm |
| A1, primo pin zoccolo sinistro | (60,4) mm |
| Primo pin zoccolo destro | (77,78;4) mm; passo lungo le file 2,54 mm |
| J1, J2, J3, pin 1 | (7,14), (7,28), (7,42) mm; ingresso cavi verso sinistra |
| D1, D2, D3, catodo | (21,62), (36,62), (51,62) mm |

Le coordinate dei footprint sono ancoraggi, non centri di aperture. Il centro USB è circa X=68,89 mm nel modello; non definisce la dimensione del foro per la spina.

Il riferimento STEP usa X a destra e **Y verso l'alto**: la PCB occupa X=0…90, Y=−70…0. Per passare dalle coordinate della tabella a STEP/AutoCAD, invertire Y e poi applicare la traslazione scelta per la PCB. Non scalare l'assieme.

## Controllo della proposta 112 × 94 × 28 mm

La proposta resta preliminare. Si assume qui che i 28 mm siano l'altezza della **sola base**, che i supporti siano alti 5 mm sopra il pavimento interno e che il coperchio da 2,5 mm appoggi sopra il bordo. Altezza chiusa risultante: **30,5 mm**. Un coperchio incassato richiede un nuovo controllo.

| Calcolo | Risultato |
| --- | --- |
| Vano in pianta, pareti da 2,5 mm | 107 × 89 mm |
| Differenza totale fra vano e PCB | 17 mm in X; 19 mm in Y |
| Faccia inferiore nominale PCB sopra il fondo esterno | 2,5 + 5 = 7,5 mm |
| Ingombro STEP dell'assieme | X=0…90; Y=−70…0; Z=−1,905…16,335 mm |
| Punto più alto del modello nel contenitore | 7,5 + 16,335 = 23,835 mm |
| Distanza teorica al coperchio appoggiato a Z=28 | 4,165 mm |
| Sporgenze modellate sotto PCB rispetto al pavimento | 5 − 1,905 = 3,095 mm di spazio residuo |

Questi sono calcoli di ingombro, **non una verifica completa delle interferenze del contenitore**. Nella successiva v02 il proprietario ha scelto per la PCB l'angolo inferiore sinistro (14,7), con Y verso l'alto, e Z inferiore 7,5. La torretta (106,6) collide con l'angolo PCB (104,7). Le precedenti riserve di 15 mm per USB e 10 mm per cavi sono ipotesi, non misure dei componenti acquistati. Anche i 4,165 mm superiori non provano che sia possibile premere BOOTSEL o afferrare ed estrarre il Pico.

Nel STEP semplificato il solo substrato è spesso 1,51 mm: l'esportazione predefinita omette rame e soldermask come geometria. **Non sostituire** per questo il valore nominale PCB di 1,6 mm. Saldature reali, tolleranze e posizione finale degli zoccoli richiedono misure fisiche.

## Controlli eseguiti e mancanti

L'assieme STEP si importa in Open CASCADE e contiene **21 solidi validi, con 21 gusci chiusi**. Sono validi anche gli STEP di dettaglio. Questi risultati riguardano i riferimenti elettronici. Per i successivi solidi AutoCAD e gli STL del contenitore, vedere i [controlli v02](preliminary/assisted-v02/README.md): mesh chiuse e dimensioni controllate, accoppiamento non verificato e collisione nota.

Quote e scelte ancora necessarie:

- Pico esatto, zoccoli e header: altezze montate, sporgenze sotto PCB e spazio di estrazione verticale/laterale.
- Spina micro-USB: larghezza, altezza, lunghezza del corpo isolante, verso d'inserimento, tratto rigido, raggio di curvatura e corsa per scollegarla. Il modello della presa non comprende la spina.
- Morsetti e fili: codice del componente effettivo, sezione e diametro esterno dei fili, ferrule eventuali, accesso del cacciavite, curvatura, passacavo e fermacavo.
- Supporti PCB: diametro esterno, tipo di fissaggio e profondità utile. Ø3,2 mm NPTH sulla PCB non è il diametro del preforo di una vite nella plastica o della sede di un inserto.
- Fissaggi coperchio distinti dai quattro supporti PCB: posizione, diametro delle torrette, inserti/dadi/filettatura, impronta di testa e rondella, utensile e distanza dal bordo.
- Viti: lunghezza sotto testa, spessori attraversati, presa utile, fondo del foro cieco e margine prima del fondo. Per una vite PCB dall'alto, penetrazione = lunghezza − spessore PCB − rondella; confrontarla con la profondità realmente disponibile. Per il coperchio usare il suo spessore e l'eventuale lamatura. Nessuna lunghezza è stata approvata.
- Stampa: materiale, ugello, orientamento, ritiri e giochi misurati con provini. Non è stata assegnata una tolleranza arbitraria ai fori.

## Screenshot reali disponibili

Sono catture della finestra KiCad del file canonico, ritagliate per mostrare soltanto il progetto. Le viste 3D sono **modelli CAD visualizzati a schermo**, non fotografie di hardware.

| Cattura | Contenuto |
| --- | --- |
| [PCB lato componenti](../../docs/images/module-monitor-pcb-top-screenshot.png) | Editor PCB reale |
| [Assieme PCB dall'alto](../../docs/images/module-monitor-pcb-3d-top-screenshot.png) | Visualizzatore 3D KiCad reale |
| [Assieme PCB obliquo](../../docs/images/module-monitor-pcb-3d-oblique-screenshot.png) | Visualizzatore 3D, zoccoli e componenti |

Le successive [sette catture reali AutoCAD del contenitore](preliminary/assisted-v02/screenshots.html) mostrano assieme, esploso, interno, base aperta, supporti dall'alto, coperchio e sezione quotata. La modellazione è assistita automatica. Le sei esportazioni KiCad preesistenti in `electronics/module-monitor/exports/images/` restano esportazioni precedenti, non nuovi screenshot.

## Riproducibilità e contributi

`extract_reference.py` legge la PCB con il Python di KiCad e richiama `kicad-cli pcb export step`; `inspect_step.py` riapre gli STEP e verifica geometria e ingombri. Gli script rifiutano di sovrascrivere risultati precedenti. Usare una nuova cartella di output per una nuova revisione. Le dipendenze di analisi sono state installate nella cartella locale di lavoro, fuori dalla repository.

Il proprietario ha fornito requisiti, proposta dimensionale e chiarimenti sui materiali disponibili. Codex ha esaminato i file esistenti, estratto quote, esportato e controllato riferimenti STEP, catturato le viste KiCad e preparato questa guida. Non sono state attribuite al proprietario modellazione automatica, fabbricazione o prove fisiche. `BOM.md` e `JOURNAL.md` non sono stati modificati. La prova fisica resta da fare.
