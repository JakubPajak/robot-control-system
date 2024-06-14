import queue
import threading
import time

from utils.message import Message
from pyPS4Controller.controller import Controller

class ManualModePad(Controller):

    def __init__(self, communication_queue , **kwargs,):
        self.communication_queue = communication_queue
        super().__init__(**kwargs)

    def on_x_press(self):
        print("X button pressed")
        message = Message("X button pressed")
        self.communication_queue.put(message)
        #time.sleep(0.5)

    def on_x_release(self):
        print("X button released")
        message = Message("X button released")
        self.communication_queue.put(message)
        #time.sleep(0.5)

    def on_circle_press(self):
        print("Circle button pressed")
        message = Message("Circle button pressed")
        self.communication_queue.put(message)
        time.sleep(0.5)
        #exit()  # Exit the program when Circle button is pressed (example)

    # Add other important actions as needed
    def on_square_press(self):
        print("Square button pressed")

    def on_triangle_press(self):
        print("Triangle button pressed")

    def on_R1_press(self):
        print("R1 button pressed")

    def on_L1_press(self):
        print("L1 button pressed")

    def on_R2_press(self, value):
        print(f"R2 button pressed with value {value}")

    def on_L2_press(self, value):
        print(f"L2 button pressed with value {value}")

    def on_options_press(self):
        print("Options button pressed")

    def on_share_press(self):
        print("Share button pressed")

    # You can also handle joystick movements if needed
    def on_L3_up(self, value):
        if value < -600:
            print("Left Up !")
            message = Message("Forward")
            self.communication_queue.put(message)
            time.sleep(0.1)

    def on_L3_down(self, value):
        pass

    def on_L3_left(self, value):
        pass

    def on_L3_right(self, value):
        pass

    # Right joystick
    def on_R3_up(self, value):
        pass

    def on_R3_down(self, value):
        pass

    def on_R3_left(self, value):
        pass

    def on_R3_right(self, value):
        pass

# controller = ManualModePad(interface="/dev/input/js0", connecting_using_ds4drv=False)
# controller.listen(timeout=60)
