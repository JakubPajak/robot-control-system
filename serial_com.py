import serial
import time

class SerialCommunication:
    
    def __init__():
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

        if ser.is_open:
            print("Serial port is open")

        ser.reset_input_buffer()
        ser.reset_output_buffer()

    def send_data():

        try:
            while True:
                input_data = input("Enter the number you want to send ")
                ser.write((input_data + '\n').encode('utf-8'))

                print("The message has been sent")
                time.sleep(2)

                if ser.in_waiting > 0:
                    rec  = ser.readline().decode('utf-8').strip()
                    print("Received: ", rec)
                else:   
                    print("No incoming data!")

        finally:
            ser.close()
                 
        
