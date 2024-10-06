import threading
import time
import os
import sys

module_path = os.path.abspath('/home/jakub/engineering_proj/robot-control-system/current_v2')
sys.path.insert(0, module_path)

from serial_communication import SerialCommunication
from auto_control_mode import AutoModeModule
from camera_module import CameraModule
from web_app.app import WebAppVisu

def mainTask(serial_com):
    main_task_is_running = True

    status = threading.Event()

    while main_task_is_running:
        print("The application has started. Please choose one of the following options:")
        print("1: Automatic mode")
        print("2: Manual mode")
        print("3: Open Operator Panel")
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
            try:
                camera_module_task = threading.Thread(target=start_web_app_task)
                camera_module_task.start()
                print("Camera task has started correctly")
            except:
                print("Exception occured during attepmt to start camera Task")


        elif choice == '5':

            if auto_control_thread and auto_control_thread.is_alive():
                status.set()
                auto_control_thread.join()

                print("Exiting ... ")
            break
            

def start_auto_control_task(serial_com, status):
    auto_module = AutoModeModule(serial_com, status)
    auto_module.selectPath()

def start_web_app_task():
    web_app = WebAppVisu()
    web_app.run()

def main():
    # serial_com = SerialCommunication()
    serial_com = 0
    mainTask(serial_com)

if __name__ == "__main__":
    main()

