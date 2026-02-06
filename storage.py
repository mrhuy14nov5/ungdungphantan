import threading
import time

class Storage:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def put(self, key, value):
        with self.lock:
            self.data[key] = (value, time.time())

    def get(self, key):
        with self.lock:
            return self.data.get(key)

    def delete(self, key):
        with self.lock:
            self.data.pop(key, None)

    def snapshot(self):
        with self.lock:
            return dict(self.data)

    def load(self, snap):
        with self.lock:
            self.data = dict(snap)
