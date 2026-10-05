# Raspberry Pi Pico / MicroPython. Prototype; hardware testing pending.
from machine import Pin
from time import ticks_ms, ticks_diff, sleep_ms
import json
from logic import Debouncer

inputs = [Pin(g, Pin.IN, Pin.PULL_UP) for g in (2, 3, 4)]
leds = [Pin(g, Pin.OUT, value=0) for g in (10, 11, 12)]
filters = [Debouncer(1, ticks_ms()) for _ in inputs]
previous = None
last_report = ticks_ms()
while True:
    now = ticks_ms()
    present = [f.update(pin.value(), now, ticks_diff) == 0
               for f, pin in zip(filters, inputs)]
    for led, state in zip(leds, present):
        led.value(int(state))
    if present != previous or ticks_diff(now, last_report) >= 1000:
        print(json.dumps({'type': 'modudeck_presence', 'trays': present}))
        previous = present[:]
        last_report = now
    sleep_ms(5)
