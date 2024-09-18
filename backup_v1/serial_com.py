import serial
import time

class SerialCommunication:
    
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

        if self.ser.is_open:
            print("Serial port is open")

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def send_data(self, data):
        try:
            
            self.ser.write(f'{data}\n'.encode('utf-8'))  # Wysyłanie liczby z zakończeniem \n
            print(f"The message {data} has been sent")
            time.sleep(2)  # Czekamy na odpowiedź

            
            if self.ser.in_waiting > 0:
                rec = self.ser.readline().decode('utf-8').strip()  # Usunięcie \r\n
                print("Received: ", rec)
                return True
            else:   
                print("No incoming data!")
                return False
        except Exception as e:
            print(f'Exception occurred during serial communication: {e}')
            return False
