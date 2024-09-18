import threading
import time
import cv2

from utils.task_state import TaskState

def open_webcam(state):
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        state.status = 'Error'
        state.message = 'Could not open webcam'
        return
    
    start_time = time.time()
    while True: 
        ret, frame = camera.read()

        if not ret:
            state.status = 'Error'
            state.message = 'Could not read frame'

        if time.time() - start_time > 5:
            state.status = 'Timeout'
            state.message = 'Task ended with timeout'
            break
    
    camera.release()
    cv2.destroyAllWindows()

    if state.status is None:
        state.status = 'Done'
        state.message = 'Task ended successfully'

