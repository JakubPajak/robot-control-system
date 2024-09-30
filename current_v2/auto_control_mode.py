import json
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
#   Each instruction is converted into a 2-byte frame, which is structured as:
#     - Byte 0: 
#           a) Bit 7 -> Action type (1 for "Turn", 0 for "forward")
#           b) Bit 5 -> Direction (0 for left, 1 for right, for turns)
#           c) Bit 5-0 -> Reserved
#     - Byte 1: 8-bit data value, either the angle for turns or the speed for forward movement.
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

        path_id = 'path2'
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

            # Access the paths dictionary using the provided string key (path_id)
            paths = data['robot_instructions']['paths']

            # Make sure the path_id exists in the dictionary
            if path_id in paths:
                selected_path = paths[path_id]
            else:
                raise ValueError(f"Path ID '{path_id}' not found in the JSON file")

            formatted_frame_table = []

            for step in selected_path:
                temp_frame = bytearray(2)  # Używamy tylko dwóch bajtów

                if step["action"] == "turn":
                    action = 1  
                    direction = 0 if step["direction"] == "left" else 1  
                    angle = step["angle"]

                    # Pierwszy bajt: akcja i kierunek
                    temp_frame[0] = (action << 6) | (direction << 5)  # Ustawienie akcji i kierunku

                    # Drugi bajt: kąt skrętu, musimy to zakodować
                    temp_frame[1] = angle & 0xFF  # Ustawienie dolnego bajtu kąta (0-255)

                elif step["action"] == "forward":
                    action = 0
                    distance = step["distance"]

                    temp_frame[0] = (action << 7)  # Ustawienie akcji

                    temp_frame[1] = distance & 0xFF  # Ustawienie dolnego bajtu prędkości (0-255)

                formatted_frame_table.append(temp_frame)

            return formatted_frame_table


    # def InterpretPathFromJson(self, path_id):
    #     with open('path.json', 'r') as file:
    #         data = json.load(file)

    #         # Access the paths dictionary using the provided string key (path_id)
    #         paths = data['robot_instructions']['paths']

    #         # Make sure the path_id exists in the dictionary
    #         if path_id in paths:
    #             selected_path = paths[path_id]
    #         else:
    #             raise ValueError(f"Path ID '{path_id}' not found in the JSON file")

    #         formatted_frame_table = []

    #         for step in selected_path:
    #             temp_frame = bytearray(2)

    #             if step["action"] == "turn":
    #                 action = 1  
    #                 direction = 0 if step["direction"] == "left" else 1  
    #                 angle = step["angle"]

    #                 temp_frame[0] = (action << 7) | (direction << 6)
    #                 temp_frame[1:] = struct.pack(">H", angle)

    #             elif step["action"] == "forward":
    #                 action = 0
    #                 speed = step["speed"]

    #                 temp_frame[0] = (action << 7)
    #                 temp_frame[1:3] = struct.pack(">H", speed)

    #             formatted_frame_table.append(temp_frame)

    #     return formatted_frame_table