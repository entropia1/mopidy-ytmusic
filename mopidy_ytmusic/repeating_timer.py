# Stolen almost directly from mopidy-gmusic
from threading import Event, Thread


class RepeatingTimer(Thread):
    def __init__(self, method, interval=0):
        Thread.__init__(self)
        self._stop_event = Event()
        self._refresh_event = Event()
        self._interval = interval
        self._method = method
        self._force = 0

    def now(self, wait=False):
        self._force = 1
        if wait:
            self._refresh_event.clear()
        self._stop_event.set()
        if wait:
            self._refresh_event.wait(timeout=60)

    def run(self):
        self._method()
        while self._interval > 0:
            ew = self._stop_event.wait(self._interval)
            if ew and not self._force:
                break
            elif self._force:
                self._stop_event.clear()
                self._force = 0
            try:
                self._method()
            finally:
                self._refresh_event.set()

    def cancel(self):
        self._stop_event.set()
