import serial
import time

####################---> Description <---##################### 
#
#   The SerialCommunication class is designed to handle communication 
#   between a Raspberry Pi and an Arduino over a serial interface.
#
#   Concept:
#   This class initializes a serial connection with a specified port and baud rate.
#   It provides a method to send binary-encoded frames to the Arduino. The frames are 
#   transmitted directly as raw bytes, which ensures that data is sent exactly as 
#   intended without conversion or encoding issues.
#
#   The `send_data` method takes a `bytearray` as input, representing a preformatted 
#   binary frame. This method writes the frame to the serial port, waits for a short 
#   period to allow for transmission, and checks if there is any response from the Arduino. 
#   If a response is received, it is read and decoded from the serial buffer.
#
########################---> End <---##########################

class SerialCommunication:
    
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 250000, timeout=1)

        if self.ser.is_open:
            print("Serial port is open")

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        #self.ser.write(bytes([0b00000000, 0x00]))

    def send_data(self, data, timeout=5):
        try:
            # Wyślij ramkę danych
            self.ser.write(data)  
            print(f"The binary message {data} has been sent")

            # Czas startowy dla timeoutu
            start_time = time.time()
            dane_str = ""
            
            # Pętla oczekiwania na odpowiedź
            while True:
                # Sprawdź, czy upłynął czas timeoutu
                if time.time() - start_time > timeout:
                    print("Timeout reached, no response from Arduino.")
                    #return False  # Zwróć False, jeśli przekroczony czas oczekiwania
                
                if self.ser.in_waiting > 0:
                    # Odczytuj dane po bajtach
                    dane = self.ser.read(self.ser.in_waiting)
                    dane_str += dane.decode('utf-8', errors='ignore')
                    print(dane_str)
                    # Sprawdź, czy wiadomość "FINISH" została odebrana
                    if "FINISH" in dane_str:
                        print('Arduino confirmed movement completion.')
                        return True

        except Exception as e:
            print(f'Exception occurred during serial communication: {e}')
            return False