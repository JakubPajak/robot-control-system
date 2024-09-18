import threading
import time
from auto_mode_module import AutoModeModule
from camera_module import open_webcam, TaskState
from manual_pad_module import ManualModePad
from serial_com import SerialCommunication
from steering_module import SteeringModule
from utils.circular_queue import CircularQueue

def main_task(communication_queue, status_queue, serial_com):
    main_control = True
    state = TaskState()
    stop_event = threading.Event()
    change_state = threading.Event()
    manual_mode_thread = None

    steering_task_thread = threading.Thread(target=start_steering_task, args=(communication_queue, stop_event))
    steering_task_thread.start()

    while main_control:
        print("Main task is running...")
        print("Select mode that you want to run")
        print("1: Automatic mode")
        print("2: Manual mode")
        print("3: Open camera")
        print("4: Exit manual mode")
        print("5: Exit app")

        choice = input()
        if choice == '1':
            print("Starting auto mode...")
            auto_mode_thread = threading.Thread(target=start_auto_task, args=(status_queue, change_state, serial_com))
            auto_mode_thread.start()

            while not change_state.is_set():
                time.sleep(0.01) 
            auto_mode_thread.join()
            print("Auto mode has finished")
        
        elif choice == '2':
            if manual_mode_thread is None or not manual_mode_thread.is_alive():
                print('2: Entering manual mode...')
                manual_mode_thread = threading.Thread(target=start_manual_mode, args=(communication_queue, stop_event, 10))
                manual_mode_thread.start()
            else:
                print('Manual mode is already running')

        elif choice == '3':
            print("Opening camera module")
            start_camera_task(state)

        elif choice == '4':
            print("Exiting the manual mode...")
            stop_event.set()  
            if manual_mode_thread:
                terminate_thread(manual_mode_thread)  

        elif choice == '5':
            if manual_mode_thread is not None and manual_mode_thread.is_alive():
                terminate_thread(manual_mode_thread)
            
            if steering_task_thread.is_alive():
                stop_event.set()
                steering_task_thread.join()
            
            if auto_mode_thread and auto_mode_thread.is_alive():
                change_state.set()
                auto_mode_thread.join()
            break

        time.sleep(1)

def start_camera_task(state):
    state.status = None
    state.message = None

    camera_thread = threading.Thread(target=open_webcam, args=(state,))
    camera_thread.start()
    camera_thread.join()

    if state.status == 'Error':
        print(f"Camera task ended with error: {state.message}")
    elif state.status == 'Timeout':
        print(f"Camera task ended with timeout: {state.message}")
    elif state.status == 'Done':
        print(f"Camera task ended successfully: {state.message}")

def start_manual_mode(communication_queue, stop_event):
    controller = ManualModePad(communication_queue=communication_queue, stop_event=stop_event, interface='/dev/input/js0', connecting_using_ds4drv=False)
    controller.listen()

def start_steering_task(communication_queue, stop_event):
    steering_module = SteeringModule(communication_queue, stop_event)
    steering_module.steering_module()

def start_auto_task(status_queue, change_status, serial_com):
    auto_module = AutoModeModule(serial_com, change_status)
    auto_module.select_path()

def terminate_thread(thread):
    import ctypes
    if not thread.is_alive():
        return
    
    tid = thread.ident
    if tid is None:
        return

    if hasattr(thread, 'native_id'):
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_ulong(tid), ctypes.py_object(SystemExit))
    else:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(SystemExit))

def main():
    communication_queue = CircularQueue(max_size=10)
    status_queue = CircularQueue(max_size=1)
    serial_com = SerialCommunication()

    main_task(communication_queue, status_queue, serial_com)

if __name__ == "__main__":
    main()
