from collections import OrderedDict
from threading import Lock


class LRUCache:
    def __init__(self, capacity: int = 10000):
        self.capacity = capacity
        self._data = OrderedDict()
        self._lock = Lock()

    def get(self, key):
        with self._lock:
            if key not in self._data:
                return None
            # mark as recently used
            self._data.move_to_end(key)
            return self._data[key]

    def put(self, key, value):
        with self._lock:
            if key in self._data:
                self._data.move_to_end(key)
            self._data[key] = value
            if len(self._data) > self.capacity:
                # evict least recently used
                self._data.popitem(last=False)
