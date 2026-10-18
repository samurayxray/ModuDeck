# Modellazione personale in AutoCAD — traccia preliminare

Guida preparata con assistenza automatica. I passaggi seguenti **non sono stati eseguiti**. Salva il lavoro effettivamente fatto e descrivilo con parole tue; non registrare come lavoro personale l'esportazione STEP o i controlli automatici.

1. Crea un nuovo disegno dedicato, senza sovrascrivere `Disegno1` o altri file. Imposta unità di inserimento in millimetri e UCS World. Salvalo come `preliminary/module-monitor-enclosure-preliminary-v01.dwg`. Prima di una revisione conserva una copia con numero versione diverso.

2. Costruisci personalmente la base preliminare. Con il comando internazionale `_BOX`, crea un solido dal punto (0,0,0) al punto (112,94,0), altezza 28. Crea il volume interno da (2.5,2.5,2.5) a (109.5,91.5,2.5), altezza 25.5, e sottrailo dal primo con `_SUBTRACT`, selezionando prima la base e poi il volume da togliere. Controlla con misure e sezione che restino fondo e pareti da 2,5 mm. Sono quote proposte, non quote approvate per la stampa.

3. Importa come riferimento `../reference/module-monitor-pcb-assembly.step` dal menu di importazione di AutoCAD. La conversione supportata dipende dai traduttori installati: verifica che compaia l'assieme completo e controlla la dimensione 90 × 70 mm. Non cambiare estensione al file e non scalarlo per farlo entrare. Se l'importazione STEP non è disponibile, conserva il riferimento e continua il controllo in KiCad; non dichiarare un'importazione riuscita.

4. Metti il riferimento su un layer separato identificato come `PCB_REFERENCE`. Le coordinate STEP sono X=0…90 e Y=−70…0: scegli la traslazione XY dopo aver ragionato sul lato USB e sull'uscita dei tre cavi. Porta il fondo del riferimento a Z=7,5 soltanto se mantieni fondo da 2,5 mm e supporti da 5 mm. Le coordinate dei fori STEP sono (5,−5), (85,−5), (5,−65), (85,−65); applica la stessa traslazione al centro dei supporti. Non usare queste coordinate direttamente come coordinate esterne della scatola.

5. Progetta i quattro supporti PCB alti 5 mm, separatamente dai fissaggi del coperchio. Decidi diametri, tipo di vite/inserto e profondità dei fori in base ai componenti scelti. Verifica distanza da saldature, impronta della testa della vite e accesso dell'utensile. Non copiare torrette dai blueprint AI senza controllarle sulla PCB.

6. Crea un secondo solido per il coperchio, 112 × 94 × 2,5 mm; tienilo identificabile e separato dalla base. Per la verifica in assieme, l'ipotesi corrente lo appoggia a Z=28, con sommità a Z=30,5. Per la lavorazione puoi tenerlo spostato lateralmente. Disegna i suoi fissaggi soltanto dopo avere scelto posizione e tipo delle torrette dedicate. Non unire base e coperchio in un solo solido.

7. Per ora lascia USB e passaggi cavi **da dimensionare**. Quando avrai scelto i componenti reali, raccogli le misure elencate nel README e disegna le aperture. Prova anche il movimento di inserimento/scollegamento della spina, la curvatura dei fili e l'accesso del cacciavite ai morsetti. Decidi se BOOTSEL si usa a coperchio rimosso o attraverso un accesso dedicato; verifica la rimozione del Pico dagli zoccoli e dell'intera PCB dalla base.

8. Prima degli export, controlla che base e coperchio risultino solidi 3D chiusi, con volume positivo. Usa le funzioni di controllo solidi e interferenza disponibili in AutoCAD; verifica separatamente PCB/base, PCB/coperchio, PCB/torrette e tutti i fissaggi. Non applicare un esito positivo all'intero progetto se hai controllato soltanto il parallelepipedo di ingombro. Conserva un modello completo e crea viste/sezioni senza distruggere la geometria originale.

9. Esporta STL **soltanto** dei pezzi stampati selezionati, base e coperchio separati, in coordinate millimetriche. STL non contiene un'unità affidabile: nel programma di controllo/slicer verifica importazione a scala 1:1, dimensioni, mesh chiusa, normali coerenti e assenza di bordi aperti/autointersezioni. Per la proposta senza modifiche esterne, gli ingombri attesi sono 112 × 94 × 28 mm per la base e 112 × 94 × 2,5 mm per il coperchio. Confrontali nuovamente se aggiungi geometria esterna. Escludi PCB e componenti acquistati. Non aggiungere supporti di stampa del slicer agli STL di progetto.

10. Conserva sempre il DWG. Esporta anche STEP dei soli pezzi stampati soltanto se l'applicazione offre un traduttore valido; riapri l'esportazione per verificarla. Il fatto che AutoCAD importi STEP non dimostra che possa esportarlo. Non rinominare STL/DWG in `.step`.

11. Salva sei screenshot reali in `../../docs/images/`: `module-monitor-enclosure-preliminary-isometric.png`, `...-base-open.png`, `...-supports-fasteners.png`, `...-lid.png`, `...-pcb-section.png`, `...-dimensions.png`. Inquadra soltanto il modello; le quote e le sezioni devono venire dal CAD. Le didascalie devono dire **modello CAD preliminare**, senza chiamarlo foto o pezzo costruito.

12. Una revisione può passare in una futura cartella `verified/` soltanto dopo controlli documentati e riproducibili di geometria, interferenze, fissaggi e STL. Indica separatamente `CAD verificato` e `prova fisica eseguita/non eseguita`: una verifica software non equivale a una prova di stampa, montaggio o utilizzo.

Primo passo pratico: realizza e salva soltanto la base cava del punto 2. Poi controlliamo insieme lo stato effettivo prima di aggiungere supporti e aperture.
