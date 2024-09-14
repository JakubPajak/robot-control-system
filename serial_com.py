import serial
import time

class SerialCommunication:
    
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

        if self.ser.is_open:
            print("Serial port is open")

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def send_data(self):
        dir_table = [1, 2, 5, 0]
        i = 0

        try:
            while True:
                self.ser.write(('{dir_table[i]}' + '\n').encode('utf-8'))

                print("The message has been sent")
                time.sleep(2)

                if self.ser.in_waiting > 0:
                    rec  = self.ser.readline().decode('utf-8').strip()
                    print("Received: ", rec)
                    i += 1
                else:   
                    print("No incoming data!")

        finally:
            self.ser.close()
                 
        
