# Contenitore Module Monitor — CAD assistito preliminare v02

Modellazione automatica eseguita da Codex in AutoCAD 2026 il 18 ottobre 2026, su richiesta del proprietario. Il proprietario ha fornito quote e coordinate. Questa revisione non viene attribuita a modellazione personale, fabbricazione o prove fisiche del proprietario; non sono registrate ore.

**Accoppiamento non verificato: esiste un'interferenza nota.** La torretta coperchio centrata in (106,6), raggio 4 mm, invade l'angolo PCB (104,7): distanza √5 = 2,236 mm. La PCB occupa Z=7,5…9,1 e la torretta Z=2,5…28. Le coordinate richieste sono conservate per consentire una correzione esplicita. Non usare questi STL come pezzi pronti.

## File

| File | Contenuto |
| --- | --- |
| [assembly-preliminary-v02.dwg](assembly-preliminary-v02.dwg) | Assieme allineato, tre solidi distinti: base, coperchio, sagoma PCB |
| [base-preliminary-v02.dwg](base-preliminary-v02.dwg) | Base con quattro supporti PCB e quattro torrette coperchio, un unico solido |
| [lid-preliminary-v02.dwg](lid-preliminary-v02.dwg) | Coperchio separato con quattro fori Ø3,2; conservato a Z=28…30,5 |
| [interior-review-preliminary-v02.dwg](interior-review-preliminary-v02.dwg) | Copia dell'assieme con layer COPERCHIO spento |
| [exploded-review-preliminary-v02.dwg](exploded-review-preliminary-v02.dwg) | Copia esplosa: solo il coperchio traslato +40 mm in Z |
| [section-y12-review-preliminary-v02.dwg](section-y12-review-preliminary-v02.dwg) | Copia sezionata a Y=12, mantenuta la metà Y>12, quote in XZ |
| [base-preliminary-mm-v02.stl](base-preliminary-mm-v02.stl) | Solo base, interpretare le coordinate in millimetri |
| [lid-preliminary-mm-v02.stl](lid-preliminary-mm-v02.stl) | Solo coperchio, copia traslata a Z=0…2,5 per esportazione |
| [screenshots.html](screenshots.html) | Galleria locale di sette catture reali AutoCAD |

I DWG sono file nativi AutoCAD, gli STL sono esportazioni effettive STLOUT, senza cambio di estensione. Il DWG v01 preesistente è stato copiato fuori dalla repository prima della modellazione; i risultati sono salvati con nomi nuovi v02.

## Geometria e riferimento

Millimetri, UCS World: origine nell'angolo esterno inferiore sinistro della base, X a destra, Y positivo sul piano della base, Z positivo in altezza.

- Base 112 × 94 × 28; pavimento e pareti 2,5; cavità 107 × 89 × 25,5, dal punto (2,5;2,5;2,5).
- Supporti PCB Ø7, da Z=2,5 a 7,5, centri (19,12), (99,12), (19,72), (99,72).
- Torrette coperchio Ø8, da Z=2,5 a 28, centri (6,6), (106,6), (6,88), (106,88). Nessun preforo definito.
- Coperchio 112 × 94 × 2,5, a Z=28…30,5, quattro fori passanti Ø3,2 coassiali alle torrette.
- Sagoma PCB 90 × 70 × 1,6, angolo (14,7), faccia inferiore Z=7,5; quattro fori Ø3,2. Contorno, spessore e interassi 80 × 60 verificati sulla [PCB KiCad canonica](../../../../electronics/module-monitor/ModuDeck-Module-Monitor.kicad_pcb).
- Layer BASE, COPERCHIO, PCB_RIFERIMENTO e QUOTE. Le quote dell'assieme sono su un layer separato, spento nelle catture pulite; la copia di sezione conserva le quote visibili.

La sagoma verde è il riferimento nominale della scheda, senza i solidi di Pico, morsetti o altri componenti. L'assieme elettronico STEP reale rimane in [reference/](../../reference/). Non è stata verificata l'estrazione della scheda, l'accessibilità BOOTSEL o l'assenza di interferenze con tutti i componenti.

## Controlli effettivi

[stl-checks.json](stl-checks.json): entrambe le mesh sono chiuse, con orientamento coerente e un solo componente connesso. Ingombri STL: base 112 × 94 × 28 mm, coperchio 112 × 94 × 2,5 mm, scarto dimensionale inferiore a 0,0001 mm. Gli STL non codificano un'unità: importarli in mm. La verifica della mesh non certifica l'accoppiamento.

I quattro rapporti `.mpr` sono MASSPROP nativi AutoCAD. Volume base con supporti: 57577,4278 mm³; coperchio: 26239,5752 mm³. La tessellazione STL introduce un piccolo scarto di volume.

Restano da verificare: Pico e zoccoli effettivi, spina USB completa e accesso BOOTSEL, morsetti/cavi e utensili, rimozione PCB, fissaggi e prefori, lunghezze viti/profondità utili, tolleranze e materiale di stampa. Nessuna apertura USB/LED/cavi è stata inventata. Il proprietario dispone solo del PC; la prova fisica resta da fare. Non è stato esportato uno STEP del contenitore.

## Catture e riproducibilità

[Tracciabilità delle sette catture](capture-provenance.json): fonte, hash e rettangolo di ritaglio. I PNG in [docs/images/](../../../../docs/images/) sono ritagli di vere finestre AutoCAD; nessuna immagine generativa. Le immagini mostrano CAD preliminare, non oggetti costruiti.

[build-native.scr](build-native.scr) contiene le operazioni native BOX, SUBTRACT, CYLINDER e UNION. La prima esecuzione si è arrestata durante l'esportazione dopo WBLOCK; i log `build-native-output*` conservano quell'errore. [finish-native.scr](finish-native.scr) ha recuperato le entità per layer e completato le esportazioni e le viste: [log concluso con successo](finish-native-output.log). Il generatore principale è stato poi corretto per riacquisire i riferimenti, ma non rieseguito integralmente. Riprodurre in una cartella nuova, senza sovrascrivere questi risultati.
