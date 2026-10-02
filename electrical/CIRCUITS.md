# ModuDeck circuits — revision 0.2

No phone or dialing keypad. These are precise connection drawings for the indicated prototype topology, not tested PCB designs.

- [S1 — Pico LED and button](s1-pico-test.svg): U1 original Raspberry Pi Pico powered through built-in USB; GP0 -> 1 kΩ R1 -> red LED anode; LED cathode -> GND. GP1 -> SW1 normally-open button -> GND. GP1 also connects through 10 kΩ R2 to U1 3V3. No connection between GP1 and the LED ground wire where they cross. Firmware: GP0 output initially LOW; GP1 input; software debounce. No GPIO can be connected to USB 5 V. Use GPIO labels and verify actual header positions in the Pico datasheet.
- [S2 — standard USB cable](s2-usb-cable.svg): USB-A pin 1 to Micro-B pin 1 VBUS; 2 to 2 D-; 3 to 3 D+; 4 to 5 GND. Micro-B pin 4 ID unconnected. Use a factory-made data cable; this drawing is not a custom high-speed PCB layout.
- [S3 — system wiring](s3-system-wiring.svg): Pi4 on its own 5.1V/3A supply, independently powered display and self-powered hub; hub upstream backfeed prevention required. Supplies' positive rails are not tied together. Display and hub models, input polarity and combined power behavior still need selection.

S1 is an optional bench demonstrator; trays remain empty unless this board is fitted. R1 and R2: 1/4W resistors are sufficient for this 3.3V topology. LED current depends on forward voltage (roughly 1.3mA for a 2.0V LED). LED/button circuit is not a power switch or a complete USB identification implementation.

Updated S1 uses an explicit external pull-up, replacing the internal-pull-up assumption in revision 0.1. First prototype only uses factory-made USB cables and module sockets. No battery charger, custom power/data connector, regulator PCB or internal mains circuit is defined. No electrical bench test or KiCad ERC has been run.

References: https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf ; https://www.raspberrypi.com/products/type-c-power-supply/ ; https://www.raspberrypi.com/documentation/computers/raspberry-pi.html
