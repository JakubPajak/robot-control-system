

class AutoModeModule:
    def __init__(self, serial_com, stop_event):
        self.serial_com = serial_com
        self.stop_event = stop_event

        
    def select_path(self):
        status = False
        path = [100, 20, 50]
        for i in range(len(path)):
            while not status:
                status = self.serial_com.send_data(path[i])
            print(f'Order nr {i} have been performed with value: {path[i]}')
            status = False

        self.stop_event.set()

