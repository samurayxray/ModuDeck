# Provisional mechanical definition — Rev 1.0

The routed PCB outline is **90 x 70mm**, rectangular, with a nominal **1.6mm** FR4 thickness. It uses two copper layers and assumes standard 35um (1oz) copper, solder mask on both faces and top/bottom silkscreen. Signal tracks are 0.30mm; the minimum rule is 0.25mm track/clearance and 0.50mm copper-to-edge. No blind or buried vias are used. Ground pours are on both faces with 0.30mm clearance and thermal reliefs. The exported board has 105 track segments and no vias: through-hole pads provide the required face connections.

The 90 x 70mm dimension is measured between outline centre lines. KiCad's Gerber job bounding box includes the 0.05mm outline drawing stroke and therefore reports 90.05 x 70.05mm; this is not a different board outline. Surface finish is not specified in the job file and remains a fabricator/quote choice.

Coordinates below use the **top-left outline corner** as (0,0), viewed from the component side with USB at the top. KiCad's absolute outline is (100,50)-(190,120)mm.

| Feature | Position / dimension |
|---|---|
| H1, H2, H3, H4 | (5,5), (85,5), (5,65), (85,65)mm |
| Mounting holes | Four 3.20mm NPTH for M3; 80 x 60mm centre spacing |
| Screw copper keepout | 7.0mm diameter on both copper layers; tracks/vias/pours prohibited |
| Pico left socket / pin 1 | (60,4)mm; pins 1-20 run downward |
| Pico right socket / pin 40 | (77.78,4)mm; pins 40-21 run downward |
| Socket pitch | 2.54mm; rows 17.78mm apart; 1.0mm drills |
| Pico USB | Faces top edge, centred near x=68.89mm; elevated above carrier on sockets |
| J1, J2, J3 pin 1 | (7,14), (7,28), (7,42)mm |
| J1, J2, J3 pin 2 | 5.08mm below each pin 1; wire entry toward left edge |
| LED cathodes D1-D3 | (21,62), (36,62), (51,62)mm; anodes 2.54mm to the right |

The original Pico is 51 x 21mm. Its USB connector and BOOTSEL remain unobstructed from above. The connector is slightly inset from the carrier's top edge and elevated: USB access relies on an enclosure opening and cable clearance, not a flush carrier-edge connector. Reserve approximately **15mm beyond the top edge** for the USB plug/cable and **10mm beyond the left edge** for switch wires; these are provisional allowances to check with the actual cables. Keep at least **18mm above the PCB top surface** for the Pico/socket and terminal assembly and at least **5mm below** for solder tails and standoffs. The model uses an 8.5mm socket body plus Pico male headers; actual seating height must be measured. Do not place an enclosure rib over BOOTSEL or the Pico removal area.

No final bay dimensions were supplied. This board has **not** been checked inside ModuDeck or printed at 1:1 scale for a physical fit test. To validate fit, measure the bay's usable width/depth/height, mounting boss coordinates, USB opening and plug envelope, LED viewing locations, switch travel/overtravel and cable paths. The 90 x 70mm outline, hole pattern and component locations can then be revised in the editable KiCad PCB. Eight M3x6 screws and four M3 5mm nylon standoffs are a provisional mounting suggestion, not a verified enclosure specification.

No fabricated board, assembled parts, battery charging, external supply or PC power-output connection is represented or tested. The unused VBUS/VSYS socket pads have no carrier traces. Use the Pico micro-USB connection as the sole supply/data path.
