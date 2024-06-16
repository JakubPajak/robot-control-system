from collections import deque
import threading
import time


class CircularQueue:
    def __init__(self, max_size):
        self.__queue = deque(maxlen=max_size)
        self.lock = threading.Lock()

    def put(self, item):
        with self.lock:
            self.__queue.append(item)
    
    def get(self):
        with self.lock:
            if len(self.__queue) == 0:
                return None
            return self.__queue.popleft()
        
