import subprocess
import os

####################---> Description <---##################### 
#
#   The ArduinoUploader class is designed to upload Arduino sketches
#   to an Arduino board from a Raspberry Pi using the avrdude tool.
#
#   Concept:
#   This class uses the `avrdude` command-line utility to program an Arduino 
#   board. It requires the path to the compiled hex file and the serial port 
#   to which the Arduino is connected. The `upload` method constructs the 
#   `avrdude` command with the necessary parameters and executes it to 
#   upload the sketch to the Arduino.
#
########################---> End <---##########################

class ArduinoUploader:
    def __init__(self, serial_port, board_type, programmer_type='arduino'):
        self.serial_port = serial_port
        self.board_type = board_type
        self.programmer_type = programmer_type
        self.avrdude_path = '/usr/bin/avrdude'  # Path to avrdude executable
        self.configuration_file = '/etc/avrdude.conf'  # Path to avrdude configuration file
    
    def upload(self, hex_file_path):
        if not os.path.isfile(hex_file_path):
            print(f"Error: Hex file '{hex_file_path}' does not exist.")
            return False
        
        avrdude_command = [
            self.avrdude_path,
            '-C', self.configuration_file,
            '-v',  # Verbose output
            '-patmega328p',  # Change this to your board's MCU
            '-carduino',  # Use the Arduino as the programmer
            '-P', self.serial_port,
            '-b115200',  # Baud rate
            '-D',  # Disable auto erase
            '-Uflash:w:{0}:i'.format(hex_file_path)  # Write hex file
        ]

        try:
            subprocess.run(avrdude_command, check=True)
            print(f"Successfully uploaded {hex_file_path} to {self.board_type} on port {self.serial_port}.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during upload: {e}")
            return False

# Example usage:
if __name__ == "__main__":
    uploader = ArduinoUploader(serial_port='/dev/ttyUSB0', board_type='arduino')
    uploader.upload('/path/to/your/sketch.hex')
