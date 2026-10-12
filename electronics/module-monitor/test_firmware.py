"""Host simulation of the actual main.py loop; no Pico or USB device involved."""
import contextlib
import io
import itertools
import json
from pathlib import Path
import runpy
import sys
import types
import unittest
from unittest.mock import patch

from firmware.logic import Debouncer


class DebounceTests(unittest.TestCase):
    def test_bounce_and_exact_boundary(self):
        f = Debouncer(1, 0)
        for raw, now, expected in [(0, 10, 1), (1, 20, 1), (0, 25, 1),
                                   (0, 54, 1), (0, 55, 0), (1, 60, 0),
                                   (1, 89, 0), (1, 90, 1)]:
            self.assertEqual(f.update(raw, now, lambda a,b: a-b), expected)

    def test_timer_wrap(self):
        f = Debouncer(1, 250)
        diff = lambda a,b: ((a-b+128) % 256)-128
        self.assertEqual(f.update(0, 250, diff), 1)
        self.assertEqual(f.update(0, 23, diff), 1)
        self.assertEqual(f.update(0, 24, diff), 0)

    def test_channels_are_independent(self):
        filters = [Debouncer(1,0) for _ in range(3)]
        for t in range(0, 101, 5):
            raw = [0, (t//5)%2, 1]
            stable = [f.update(x,t,lambda a,b:a-b) for f,x in zip(filters,raw)]
        self.assertEqual(stable, [0,1,1])


class LoopTests(unittest.TestCase):
    def simulate(self, pattern, duration, start=0):
        clock = [0]; pins = {}; writes = []; reports = []; wrap = 1 << 16

        class StopSimulation(Exception): pass
        class Pin:
            IN = 0; OUT = 1
            def __init__(self, gpio, mode, pull=None, value=None):
                self.gpio = gpio; self.mode = mode; self.state = value
                pins[gpio] = self
                if mode == self.IN:
                    if pull is not None: raise AssertionError('Internal pull enabled')
            def value(self, value=None):
                if value is not None:
                    self.state = value
                    writes.append((clock[0], self.gpio, value))
                if self.mode == self.IN:
                    return 0 if pattern(clock[0])[(2,3,4).index(self.gpio)] else 1
                return self.state

        def sleep_ms(ms):
            self.assertEqual(ms, 5)
            clock[0] += ms
            if clock[0] >= duration: raise StopSimulation()
        def report(s):
            obj = json.loads(s)
            self.assertEqual(obj['type'], 'modudeck_presence')
            self.assertEqual(len(obj['trays']), 3)
            self.assertTrue(all(isinstance(x,bool) for x in obj['trays']))
            self.assertEqual([pins[g].state for g in (10,11,12)], [int(x) for x in obj['trays']])
            reports.append((clock[0], tuple(obj['trays'])))

        machine = types.ModuleType('machine'); machine.Pin = Pin
        time = types.ModuleType('time')
        time.ticks_ms = lambda: (start + clock[0]) % wrap
        time.ticks_diff = lambda a,b: ((a-b+wrap//2)%wrap)-wrap//2
        time.sleep_ms = sleep_ms
        firmware = Path(__file__).parent/'firmware'
        with patch.dict(sys.modules, {'machine':machine, 'time':time}), patch('builtins.print', report):
            sys.path.insert(0,str(firmware))
            try:
                with self.assertRaises(StopSimulation):
                    runpy.run_path(str(firmware/'main.py'), run_name='__main__')
            finally:
                sys.path.pop(0)
        self.assertEqual(set(pins), {2,3,4,10,11,12})
        self.assertEqual([pins[g].state for g in (10,11,12)], [0,0,0])
        return reports

    def test_all_eight_states_and_led_mapping(self):
        patterns = list(itertools.product([False,True],repeat=3))
        r = self.simulate(lambda t: patterns[min(t//100,7)], 800)
        self.assertEqual([state for _,state in r], patterns)
        self.assertEqual([t for t,_ in r], [0,130,230,330,430,530,630,730])

    def test_startup_closed_bounce_and_release(self):
        def pattern(t):
            if t < 60: return (True,False,False)
            if t < 90: return ((t//5)%2 == 0,False,False)
            return (False,False,False)
        self.assertEqual(self.simulate(pattern,200),
                         [(0,(False,False,False)),(30,(True,False,False)),(115,(False,False,False))])

    def test_heartbeat_survives_wrap_without_duplicates(self):
        r = self.simulate(lambda t:(False,False,False), 3100, start=65500)
        self.assertEqual([t for t,_ in r], [0,1000,2000,3000])


if __name__ == '__main__':
    unittest.main(verbosity=2)
