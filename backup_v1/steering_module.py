import threading
import time
import serial
from utils.message import Message
from utils.circular_queue import CircularQueue


class SteeringModule:
    def __init__(self, communication_queue, stop_event):
        self.communication_queue = communication_queue
        self.stop_event = stop_event

    def steering_module(self):
        while not self.stop_event.is_set():
            message = self.communication_queue.get()
            if message:
                print(f"Received message from ManualModePad: {message.content}")
            time.sleep(0.01)
        if self.stop_event.is_set():
            print("Event received - ending the function")


