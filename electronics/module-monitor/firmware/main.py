# Original Raspberry Pi Pico / MicroPython. Hardware testing pending.
from machine import Pin
from time import ticks_ms, ticks_diff, sleep_ms
import json
from logic import Debouncer

INPUT_GPIOS = (2, 3, 4)
LED_GPIOS = (10, 11, 12)
DEBOUNCE_MS = 30
REPORT_MS = 1000
POLL_MS = 5


def run():
    # Board has external 10k pull-ups; disable internal pulls explicitly.
    inputs = [Pin(g, Pin.IN, pull=None) for g in INPUT_GPIOS]
    leds = [Pin(g, Pin.OUT, value=0) for g in LED_GPIOS]
    filters = [Debouncer(1, ticks_ms(), DEBOUNCE_MS) for _ in inputs]
    previous = None
    last_report = ticks_ms()
    try:
        while True:
            now = ticks_ms()
            present = [f.update(pin.value(), now, ticks_diff) == 0
                       for f, pin in zip(filters, inputs)]
            for led, state in zip(leds, present):
                led.value(int(state))
            if present != previous or ticks_diff(now, last_report) >= REPORT_MS:
                # Official RP2 MicroPython stdout uses USB CDC/REPL serial.
                print(json.dumps({'type': 'modudeck_presence', 'trays': present}))
                previous = present[:]
                last_report = now
            sleep_ms(POLL_MS)
    finally:
        for led in leds:
            led.value(0)


if __name__ == '__main__':
    run()
