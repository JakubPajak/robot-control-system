from flask import Flask, render_template, Response
import cv2

import os
import sys

module_path = os.path.abspath('/home/jakub/engineering_proj/robot-control-system/current_v2')
sys.path.insert(0, module_path)

from control_system.camera_module import CameraModule

class WebAppVisu:
    def __init__(self):
        self.app = Flask(__name__)
        self.camera = CameraModule()

        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/video', 'video', self.video)

    def generate_frames(self):
        while True:
            success, frame = self.camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def index(self):
        return render_template('index.html')

    def video(self):
        return Response(self.camera.process_image(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    def run(self):
        self.app.run(host='0.0.0.0', port=5000)

