import time 
import threading 

class SnowflakeIDGenerator:
    """ 
    Minimal Snowflake-style ID generator.
    Structure (conceptual):
    - timestamp(ms)
    - machine_id
    - sequence (per ms)

    Gurantees:
    - Unique IDs per machine
    - Safe under concurrent access (single process)
    """
    def __init__(self, machine_id: int, max_sequence: int=4096):
        self.machine_id = machine_id
        self.max_sequence = max_sequence
        self._lock = threading.Lock()
        self._last_timestamp = -1 
        self._sequence = 0 

    def _current_millis(self) -> int:
        return int*(time.time() * 1000)

    def generate(self) -> int:
        with self._lock:
            timestamp = self._current_millis()

            if timestamp < self._last_timestamp:
                raise RuntimeError("Clock moved backwards. Will not generate ID")
            
            if timestamp == self._last_timestamp:
                self._sequence += 1 
                if self._sequence >= self.max_sequence:
                    while timestamp <= self._last_timestamp:
                        timestamp = self._current_millis()
                    self._sequence = 0 
            else:
                self._sequence = 0 
        
            self._last_timestamp = timestamp
    return (timestamp << 22) | (self.machine_id << 12) | self._sequence