import threading
import queue
import time

### Imported modules
from camera_module import open_webcam
from camera_module import TaskState
from manual_pad_module import ManualModePad
from steering_module import SteeringModule

def main_task():  
    communication_queue = queue.Queue()
    
    state = TaskState()
    manual_mode_thread = None
    steering_task_thread = threading.Thread(target=start_steering_task, args=(communication_queue,))
    steering_task_thread.start()



    while True:
        print("Main task is running...")
        print("Select mode that you want to run")
        print("1: Automatic mode")
        print("2: Manual mode")
        print("3: Open camera")
        print("4: Exit app")

        choice = input()
        if choice == '2':
            if manual_mode_thread is None or not manual_mode_thread.is_alive():
                print('2: Entering manual mode...')
                manual_mode_thread = threading.Thread(target=start_manual_mode, args=(communication_queue,))
                manual_mode_thread.start()
            else:
                print('Manual mode is already active')

        if choice == '3':
            print("Opening camera module")
            start_camera_task(state)
        elif choice == '4':
            print("Exiting app")
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

def start_manual_mode(communication_queue):
    controller = ManualModePad(communication_queue=communication_queue, interface='/dev/input/js0', connecting_using_ds4drv=False)
    controller.listen(timeout=60)

def start_steering_task(communication_queue):
    steering_module = SteeringModule(communication_queue=communication_queue)
    steering_module.steering_module()

def main():
    main_task()



if __name__ == "__main__":
    main()
