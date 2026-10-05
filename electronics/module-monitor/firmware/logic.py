class Debouncer:
    def __init__(self, initial, now, delay_ms=30):
        self.stable = initial
        self.candidate = initial
        self.since = now
        self.delay_ms = delay_ms

    def update(self, raw, now, ticks_diff):
        if raw != self.candidate:
            self.candidate = raw
            self.since = now
        if self.candidate != self.stable and ticks_diff(now, self.since) >= self.delay_ms:
            self.stable = self.candidate
        return self.stable
