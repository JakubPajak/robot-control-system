import json
import struct

from ardu_upload_module import ArduinoUploader

####################---> Description <---##################### 
#
#   The AutoModeModule class is responsible for managing the correct steering
#   for robot in auto mode - without external input.
#
#   Concept:
#   This module reads movement instructions from a JSON file, converts them 
#   into binary-encoded frames, and sends these frames over a serial interface 
#   to an Arduino for execution. The path is predefined in the JSON file and 
#   consists of actions like "Turn" and "forward".
#
#   Each instruction is converted into a 5-byte frame, which is structured as:
#     - Byte 0: 
#           a) Bit 7 -> Action type (1 for "Turn", 0 for "forward")
#            b) Bit 6 -> Direction (0 for left, 1 for right, for turns)
#            c) Bit 5-0 -> Reserved
#     - Byte 1-2: 16-bit data value, either the angle for turns or the speed for forward movement.
#
########################---> End <---##########################

class AutoModeModule:
    def __init__(self, serial_com, status):
        self.serial_com = serial_com
        self.status = status

        # During __init__ the proper code must be uploaded to Arduino 
        # This will ensure that correct actions will be performed even after 
        # manual mode previously uploaded. 

        # uploader = ArduinoUploader(serial_port='/dev/ttyUSB0', board_type='arduino')
        # uploader.upload('/path/to/your/sketch.hex')

        
    def selectPath(self):
        status = False

        # Here must be added section responsible for managing the sequence 
        # and for recognizing which path to choose SO
        # camera class must have its connection

        path_id = 'path1'
        path = self.InterpretPathFromJson(path_id)
        for i in range(len(path)):
            while not status:
                status = self.serial_com.send_data(path[i])
            print(f'Order nr {i} have been performed with value: {path[i]}')
            status = False

        self.status.set()

    def InterpretPathFromJson(self, path_id):
        with open('path.json', 'r') as file:
            data = json.load(file)
            path = data['robot_instructions']['paths'][path_id]

            formatted_frame_table = []

            for step in path:
                temp_frame = bytearray(3)

                if step["action"] == "Turn":
                    action = 1  
                    direction = 0 if step["direction"] == "left" else 1  
                    angle = step["angle"]

                    temp_frame[0] = (action << 7) | (direction << 6)

                    temp_frame[1:3] = struct.pack(">H", angle)  

                elif step["action"] == "forward":
                    action = 0  
                    speed = step["speed"]

                    temp_frame[0] = (action << 7)

                    temp_frame[1:3] = struct.pack(">H", speed) 

                formatted_frame_table.append(temp_frame)

        return formatted_frame_table