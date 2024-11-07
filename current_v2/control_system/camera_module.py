import threading
import time
import cv2
import numpy as np
import imutils
from picamera2 import Picamera2
from libcamera import controls

# Define color boundaries in HSV space
colors = {
    'blue': [np.array([95, 255, 85]), np.array([120, 255, 255])],
    'red': [np.array([161, 165, 127]), np.array([178, 255, 255])],
    'yellow': [np.array([16, 0, 99]), np.array([39, 255, 255])],
    'green': [np.array([33, 19, 105]), np.array([77, 255, 255])],
    'white': [np.array([0, 0, 200]), np.array([180, 50, 255])],
}

# Common color for displaying labels and contours
display_color = (255, 255, 255)

def find_color(frame, points):
    mask = cv2.inRange(frame, points[0], points[1])  # Create mask with boundaries
    cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # Find contours from mask
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        area = cv2.contourArea(c)  # Calculate the area of the contour
        if area > 5000:  # Only consider large enough contours
            M = cv2.moments(c)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])  # Calculate X position
                cy = int(M['m01'] / M['m00'])  # Calculate Y position
                return c, cx, cy
    return None

class CameraModule:
    def __init__(self):
        # Initialize the Picamera2 object
        self.camera = Picamera2()

        video_config = self.camera.create_video_configuration(main={"size": (1920, 1080), "format": "RGB888"})
        self.camera.configure(video_config)
        self.camera.start()

        self.camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        # self.camera.set_controls({"AfTrigger": controls.AfTriggerEnum.Start})


    def process_image(self):
        while True:
            # Capture an image
            frame = self.camera.capture_array()
            hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)  # Convert to HSV color space
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            for name, color_bounds in colors.items():
                result = find_color(hsv, color_bounds)
                if result:
                    c, cx, cy = result
                    cv2.drawContours(frame, [c], -1, display_color, 3)
                    cv2.circle(frame, (cx, cy), 7, display_color, -1)
                    cv2.putText(frame, name, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, display_color, 2)

            # Thresholding to find square contours
            _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
                if len(approx) == 4 and cv2.contourArea(approx) > 1000:
                    x, y, w, h = cv2.boundingRect(approx)
                    aspect_ratio = float(w) / h
                    if 0.8 <= aspect_ratio <= 1.2:  
                        cv2.drawContours(frame, [approx], 0, (0, 255, 0), 3)  # Green contour for square
                        M = cv2.moments(contour)
                        if M['m00'] != 0:
                            cx = int(M['m10'] / M['m00'])
                            cy = int(M['m01'] / M['m00'])
                            cv2.putText(frame, "Square", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.6, display_color, 2)

            # Display the frame
            # cv2.imshow("Processed Frame", frame)

            # Encode and yield the frame as bytes for HTTP streaming or further processing
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Stop the camera and destroy all OpenCV windows
        self.camera.stop()
        cv2.destroyAllWindows()
