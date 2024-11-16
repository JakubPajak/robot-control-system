import json
import time
from ardu_upload_module import ArduinoUploader
from camera_module import CameraModule

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
        self.iterations = 0
        self.camera_module = CameraModule()

        # During __init__ the proper code must be uploaded to Arduino 
        # This will ensure that correct actions will be performed even after 
        # manual mode previously uploaded. 

        # uploader = ArduinoUploader(serial_port='/dev/ttyUSB0', board_type='arduino')
        # uploader.upload('/path/to/your/sketch.hex')

        
    def selectPath(self):
        # if self.iterations != 0:
        #     path0 = self.interpretPathFromJson('path0')
        #     self.executePath(path0)
        #     self.iterations += 1

        detected_color = self.camera_module.process_frame()
        path_id = self.choosePath(detected_color[4])
        path = self.interpretPathFromJson(path_id)
        self.executePath(path)

        self.selectPath()

        # while not self.status and self.iterations == 0:
        #     time.sleep(1)
        #     self.status = self.serial_com.send_data("path0")
        #     if self.status:
        #         print(f'Order nr {i} has been performed with value: {path[i]}')
        #     else:
        #         print(f'Failed to perform order nr {i}, retrying...')

        #     print(f'Order nr {i} completed successfully.')

        # detected_color = self.camera_module.process_frame()

        # path_id = self.choosePath(detected_color)
        # path = self.interpretPathFromJson(path_id)
        # self.iterations += 1

        # for i in range(len(path)):
        #     self.status = False

        #     while not self.status:
        #         time.sleep(1)
        #         self.status = self.serial_com.send_data(path[i])
        #         if self.status:
        #             print(f'Order nr {i} has been performed with value: {path[i]}')
        #         else:
        #             print(f'Failed to perform order nr {i}, retrying...')

        #     print(f'Order nr {i} completed successfully.')


    def executePath(self, path):
        for i in range(len(path)):
            status = False

            while not status:
                time.sleep(1)
                status = self.serial_com.send_data(path[i])
                if status:
                    print(f'Order nr {i} has been performed with value: {path[i]}')
                else:
                    print(f'Failed to perform order nr {i}, retrying...')

            print(f'Order nr {i} completed successfully.')

    def interpretPathFromJson(self, path_id):
        with open('path.json', 'r') as file:
            data = json.load(file)

            paths = data['robot_instructions']['paths']

            if path_id in paths:
                selected_path = paths[path_id]
            else:
                raise ValueError(f"Path ID '{path_id}' not found in the JSON file")

            formatted_frame_table = []

            for step in selected_path:
                temp_frame = bytearray(2) 

                if step["action"] == "turn":
                    action = 1  
                    direction = 0 if step["direction"] == "left" else 1  
                    angle = step["angle"]

                    temp_frame[0] = (action << 6) | (direction << 5) 

                    temp_frame[1] = angle & 0xFF  

                elif step["action"] == "forward":
                    action = 0
                    distance = step["distance"]

                    temp_frame[0] = (action << 7)  

                    temp_frame[1] = distance & 0xFF 

                elif step["action"] == "grab":
                    servo_action = 1 
                    servo_action_type = 1 if step["grab_type"] == "close" else 0  
                    temp_frame[0] = (servo_action << 4) | (servo_action_type << 3)

                formatted_frame_table.append(temp_frame)

            return formatted_frame_table
        
    def choosePath(self, detected_color):

        if(detected_color == 'red'):
            path_id = 'path1'
        elif(detected_color == 'blue'):
            path_id = 'path2'
        elif(detected_color == 'green'):
            path_id = 'path3'
        elif(detected_color == 'unknown'):
            self.status.set()

        return path_id