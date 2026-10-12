# Component selection and purchasing BOM

Public vendor listings were checked on **12 October 2026**. Values below are list prices, not a binding checkout quote. No parts were ordered. Shipping for every seller is **da verificare**: no delivery address or cart quote was used. VAT is excluded from EUR prices below. Prices can change.

| Part / references | Needed | Observed purchase quantity | MPN | Seller and observed unit price |
|---|---:|---:|---|---|
| Original Pico / A1 | 1 | 1 | SC0915 | [DigiKey](https://www.digikey.it/it/products/detail/raspberry-pi/SC0915/13684020): EUR 4.03 |
| Female sockets, included in A1 footprint | 2 | 2 | CONNFLY DS1023-1*20S21, TME ZL262-20SG | [TME](https://www.tme.eu/it/details/zl262-20sg/connettore-dell-intestazione-di-pin/connfly/ds1023-1-20s21/): EUR 0.38 |
| Male headers, soldered to Pico | 2 | 10 minimum | CONNFLY DS1021-1*20SF11-B, TME ZL201-20G | [TME international listing](https://www.tme.eu/en/details/zl201-20g/pin-headers/connfly/ds1021-1-20sf11-b/): USD 0.20 at 10; EUR price da verificare |
| 10k pull-ups / R1,R3,R5 | 3 | 3 | YAGEO CFR-25JB-52-10K | [DigiKey](https://www.digikey.it/it/products/detail/yageo/CFR-25JB-52-10K/338): EUR 0.09 |
| 1k series / R2,R4,R6,R7,R8,R9 | 6 | 6 | YAGEO CFR-25JB-52-1K | [DigiKey](https://www.digikey.it/it/products/detail/yageo/CFR-25JB-52-1K/96): EUR 0.09 |
| Red LEDs / D1-D3 | 3 | 5 minimum | Kingbright L-53LID | [TME](https://www.tme.eu/it/details/l-53lid/diodi-led-tht-rotondi/kingbright-electronic/): EUR 0.21 at 5 |
| Screw terminals / J1-J3 | 3 | 3 | Phoenix Contact 1715721 | [DigiKey](https://www.digikey.it/it/products/detail/phoenix-contact/1715721/260631): EUR 1.02 |
| External microswitch candidate | 3 | 3 | D2F-01L | [DigiKey](https://www.digikey.it/it/products/detail/aratas-america-llc/D2F-01L/83264): EUR 1.26; final suitability da verificare |

The verified EUR purchasing subtotal for Pico, female sockets, nine resistors, **five purchased LEDs** and three terminals is **EUR 9.71 excluding VAT**. This is a partial subtotal, not the project total. The candidate switches add EUR 3.78. Male headers are separately USD 2.00 for ten; no exchange rate conversion is claimed. USB data cable (candidate StarTech UUSBHAUB1M), wire lengths, PCB fabrication, eight M3 screws and four provisional 5mm insulating standoffs are included in [purchasing-bom.csv](exports/purchasing-bom.csv) with unverified prices left blank and marked **da verificare**.

The two sockets are physically separate parts but are deliberately represented by one A1 assembly footprint: left pad row 1-20 and right pad row 40-21, with 17.78mm spacing and 2.54mm pitch. Sockets are 8.5mm high. Do not solder Pico directly to the carrier. SC0915 is the original RP2040 Pico without headers; add both male strips to it. A pre-headered original Pico H SC0917 is an alternative, not an additional BOM item. It has not been substituted in the purchasing calculation.

Resistor bodies fit the DIN0207 footprint (6.3mm length, 2.5mm nominal diameter, 10.16mm formed lead spacing; 0.8mm holes). The YAGEO body is 6.3 x 2.4mm. LED lead pitch is 2.54mm and hole size 0.9mm: **pad 1 is cathode, pad 2 anode**. Phoenix 1715721 has 5.08mm pitch and recommended 1.3mm holes, matching the footprint. Screw terminals need no mating plug; the two switch wires can be removed by releasing the screws.

The external microswitch is not mounted on this PCB. D2F-01L is a sourcing candidate because tray travel and mounting geometry are not defined. Use only NO and COM, leave NC insulated. Contact reliability/life at the circuit's approximately 0.30mA, 3.3V dry-contact load is **not verified**. The exact switch, lever travel and cable lengths must be selected after measuring the trays and tested on hardware. This does not alter the requested resistor circuit.

Geometry sources: [Pico official datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf), [CONNFLY socket drawing](https://www.tme.eu/Document/951e887d7e645db1a4e49e0834499c9b/zl262-sg.pdf), [Phoenix official 1715721](https://www.phoenixcontact.com/de-de/produkte/leiterplattenklemme-mkds-15-2-508-1715721), and the linked vendor specification pages. Socket/header seating and LED polarity still require a physical assembly check.
