import threading
import queue
import time
from utils.message import Message

class SteeringModule:
    def __init__(self, communication_queue):
        self.communication_queue = communication_queue

    def steering_module(self):
        while True:
            if not self.communication_queue.empty():
                message = self.communication_queue.get()
                print(f"Received message from ManualModePad: {message.content}")
            time.sleep(0.5)
