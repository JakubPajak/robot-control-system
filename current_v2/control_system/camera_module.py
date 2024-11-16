# import threading
# import time
# import cv2
# import numpy as np
# import imutils
# from picamera2 import Picamera2
# from libcamera import controls


# colors = {
#     'red': [np.array([136, 87, 111], np.uint8), np.array([180, 255, 255], np.uint8)],
#     'blue': [np.array([90, 50, 50], np.uint8), np.array([120, 255, 220], np.uint8)],
#     'green': [np.array([25, 52, 72], np.uint8), np.array([102, 255, 255], np.uint8)],
#     #'white': [np.array([0, 0, 200]), np.array([180, 50, 255])],
# }


# # Common color for displaying labels and contours
# display_color = (255, 255, 255)

# def find_color(frame, points):
#     mask = cv2.inRange(frame, points[0], points[1])  # Create mask with boundaries

#     kernel = np.ones((5, 5), "uint8")

#     color_mask = cv2.dilate(mask, kernel)
#     result_color = cv2.bitwise_and(frame, frame, color_mask)

#     contours, hierarchy = cv2.findContours(color_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#     # ret, thresh = cv2.threshold(mask, 100, 255, cv2.THRESH_BINARY)

#     # cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # Find contours from mask
#     # cnts = imutils.grab_contours(cnts)

#     for c in contours:
#         area = cv2.contourArea(c)  # Calculate the area of the contour
#         if area > 300:  # Only consider large enough contours
#             x, y, w, h = cv2.boundingRect(c)
#             # M = cv2.moments(c)
#             # if M['m00'] != 0:
#             #     cx = int(M['m10'] / M['m00'])  # Calculate X position
#             #     cy = int(M['m01'] / M['m00'])  # Calculate Y position
#             #     return c, cx, cy
#     return None

# class CameraModule:
#     def __init__(self):
#         # Initialize the Picamera2 object
#         self.camera = Picamera2()

#         video_config = self.camera.create_video_configuration(main={"size": (1920, 1080), "format": "RGB888"})
#         self.camera.configure(video_config)
#         self.camera.start()

#         self.camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})
#         # self.camera.set_controls({"AfTrigger": controls.AfTriggerEnum.Start})


#     def process_image(self):
#         while True:
#             # Reading the video from the 
#             # webcam in image frames 
#             imageFrame = self.camera.capture_array() 

#             # Convert the imageFrame in 
#             # BGR(RGB color space) to 
#             # HSV(hue-saturation-value) 
#             # color space 
#             hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

#             # Set range for red color and 
#             # define mask 
#             red_lower = np.array([136, 87, 111], np.uint8) 
#             red_upper = np.array([180, 255, 255], np.uint8) 
#             red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

#             # Set range for green color and 
#             # define mask 
#             green_lower = np.array([25, 52, 72], np.uint8) 
#             green_upper = np.array([102, 255, 255], np.uint8) 
#             green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 

#             # Set range for blue color and 
#             # define mask 
#             blue_lower = np.array([94, 80, 2], np.uint8) 
#             blue_upper = np.array([120, 255, 255], np.uint8) 
#             blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper) 
            
#             # Morphological Transform, Dilation 
#             # for each color and bitwise_and operator 
#             # between imageFrame and mask determines 
#             # to detect only that particular color 
#             kernel = np.ones((5, 5), "uint8") 
            
#             # For red color 
#             red_mask = cv2.dilate(red_mask, kernel) 
#             res_red = cv2.bitwise_and(imageFrame, imageFrame, 
#                                     mask = red_mask) 
            
#             # For green color 
#             green_mask = cv2.dilate(green_mask, kernel) 
#             res_green = cv2.bitwise_and(imageFrame, imageFrame, 
#                                         mask = green_mask) 
            
#             # For blue color 
#             blue_mask = cv2.dilate(blue_mask, kernel) 
#             res_blue = cv2.bitwise_and(imageFrame, imageFrame, 
#                                     mask = blue_mask) 

#             # Creating contour to track red color 
#             contours, hierarchy = cv2.findContours(red_mask, 
#                                                 cv2.RETR_TREE, 
#                                                 cv2.CHAIN_APPROX_SIMPLE) 
            
#             for pic, contour in enumerate(contours): 
#                 area = cv2.contourArea(contour) 
#                 if(area > 5000): 
#                     x, y, w, h = cv2.boundingRect(contour) 
#                     imageFrame = cv2.rectangle(imageFrame, (x, y), 
#                                             (x + w, y + h), 
#                                             (0, 0, 255), 2) 
                    
#                     cv2.putText(imageFrame, "Red Colour", (x, y), 
#                                 cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
#                                 (0, 0, 255))	 

#             # Creating contour to track green color 
#             contours, hierarchy = cv2.findContours(green_mask, 
#                                                 cv2.RETR_TREE, 
#                                                 cv2.CHAIN_APPROX_SIMPLE) 
            
#             for pic, contour in enumerate(contours): 
#                 area = cv2.contourArea(contour) 
#                 if(area > 5000): 
#                     x, y, w, h = cv2.boundingRect(contour) 
#                     imageFrame = cv2.rectangle(imageFrame, (x, y), 
#                                             (x + w, y + h), 
#                                             (0, 255, 0), 2) 
                    
#                     cv2.putText(imageFrame, "Green Colour", (x, y), 
#                                 cv2.FONT_HERSHEY_SIMPLEX, 
#                                 1.0, (0, 255, 0)) 

#             # Creating contour to track blue color 
#             contours, hierarchy = cv2.findContours(blue_mask, 
#                                                 cv2.RETR_TREE, 
#                                                 cv2.CHAIN_APPROX_SIMPLE) 
#             for pic, contour in enumerate(contours): 
#                 area = cv2.contourArea(contour) 
#                 if(area > 5000): 
#                     x, y, w, h = cv2.boundingRect(contour) 
#                     imageFrame = cv2.rectangle(imageFrame, (x, y), 
#                                             (x + w, y + h), 
#                                             (255, 0, 0), 2) 
                    
#                     cv2.putText(imageFrame, "Blue Colour", (x, y), 
#                                 cv2.FONT_HERSHEY_SIMPLEX, 
#                                 1.0, (255, 0, 0)) 
                        
#             ret, buffer = cv2.imencode('.jpg', imageFrame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


import cv2
import numpy as np
from picamera2 import Picamera2
from libcamera import controls

class CameraModule:
    def __init__(self):
        # Initialize the Picamera2 object
        self.camera = Picamera2()
        video_config = self.camera.create_video_configuration(main={"size": (1920, 1080), "format": "RGB888"})
        self.camera.configure(video_config)
        self.camera.start()
        self.camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})

        # Define color ranges and labels
        self.color_ranges = {
            'red': [np.array([136, 87, 111], np.uint8), np.array([180, 255, 255], np.uint8)],
            'green': [np.array([25, 52, 72], np.uint8), np.array([102, 255, 255], np.uint8)],
            'blue': [np.array([94, 80, 2], np.uint8), np.array([120, 255, 255], np.uint8)]
        }
        self.labels = {
            'red': (0, 0, 255),
            'green': (0, 255, 0),
            'blue': (255, 0, 0)
        }
        self.kernel = np.ones((5, 5), np.uint8)  # Precompute kernel

    def process_frame(self):
        frame = self.camera.capture_array()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # detections = []
        best_detection = None
        max_area = 0 

        for color, (lower, upper) in self.color_ranges.items():
            # Create and process mask
            mask = cv2.inRange(hsv_frame, lower, upper)
            mask = cv2.dilate(mask, self.kernel)

            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                area = cv2.contourArea(contour)
                if area > max_area:  # Filter by minimum area
                    max_area = area
                    x, y, w, h = cv2.boundingRect(contour)
                    best_detection = (x, y, w, h, color)

        return best_detection

    def annotate_frame(self, frame, detections):
        for x, y, w, h, color in detections:
            cv2.rectangle(frame, (x, y), (x + w, y + h), self.labels[color], 2)
            cv2.putText(frame, f"{color.capitalize()} Colour", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.labels[color], 2)
        return frame

    def process_image(self):
        while True:
            image_frame = self.camera.capture_array()

            # Resize frame for faster processing
            resized_frame = cv2.resize(image_frame, (1920, 1080))
            detections = self.process_frame()

            # Annotate frame with detections
            output_frame = self.annotate_frame(resized_frame, detections)

            # Encode the frame for streaming
            _, buffer = cv2.imencode('.jpg', output_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
