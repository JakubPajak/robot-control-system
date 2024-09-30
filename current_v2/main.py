import threading
import time
from serial_communication import SerialCommunication
from auto_control_mode import AutoModeModule


def mainTask(serial_com):
    main_task_is_running = True

    status = threading.Event()

    while main_task_is_running:
        print("The application has started. Please choose one of the following options:")
        print("1: Automatic mode")
        print("2: Manual mode")
        print("3: Open camera")
        print("4: Exit manual mode")
        print("5: Exit app")

        choice = input()

        if choice == '1':
            try:
                auto_control_thread = threading.Thread(target=start_auto_control_task, args=(serial_com, status))
                auto_control_thread.start()
                print("Auto mode has started")

                while not status.is_set():
                    time.sleep(0.01)
                auto_control_thread.join()
                print("Auto mode has finished")
            except:
                print("Exception occured during attepmt to perform auto control")


        elif choice == '2':
            pass

        elif choice == '3':
            pass

        elif choice == '5':

            if auto_control_thread and auto_control_thread.is_alive():
                status.set()
                auto_control_thread.join()

                print("Exiting ... ")
            break
            

def start_auto_control_task(serial_com, status):
    auto_module = AutoModeModule(serial_com, status)
    auto_module.selectPath()

def main():
    serial_com = SerialCommunication()
    mainTask(serial_com)

if __name__ == "__main__":
    main()

