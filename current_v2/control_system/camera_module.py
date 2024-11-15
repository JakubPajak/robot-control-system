import threading
import time
import cv2
import numpy as np
import imutils
from picamera2 import Picamera2
from libcamera import controls


colors = {
    'red': [np.array([136, 87, 111], np.uint8), np.array([180, 255, 255], np.uint8)],
    'blue': [np.array([94, 80, 2], np.uint8), np.array([120, 255, 255], np.uint8)],
    'green': [np.array([25, 52, 72], np.uint8), np.array([102, 255, 255], np.uint8)],
    #'white': [np.array([0, 0, 200]), np.array([180, 50, 255])],
}



# Common color for displaying labels and contours
display_color = (255, 255, 255)

def find_color(frame, points):
    mask = cv2.inRange(frame, points[0], points[1])  # Create mask with boundaries

    kernel = np.ones((5, 5), "uint8")

    color_mask = cv2.dilate(mask, kernel)
    result_color = cv2.bitwise_and(frame, frame, color_mask)

    contours, hierarchy = cv2.findContours(color_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # ret, thresh = cv2.threshold(mask, 100, 255, cv2.THRESH_BINARY)

    # cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # Find contours from mask
    # cnts = imutils.grab_contours(cnts)

    for c in contours:
        area = cv2.contourArea(c)  # Calculate the area of the contour
        if area > 300:  # Only consider large enough contours
            x, y, w, h = cv2.boundingRect(c)
            # M = cv2.moments(c)
            # if M['m00'] != 0:
            #     cx = int(M['m10'] / M['m00'])  # Calculate X position
            #     cy = int(M['m01'] / M['m00'])  # Calculate Y position
            #     return c, cx, cy
    return None

class CameraModule:
    def __init__(self):
        # Initialize the Picamera2 object
        self.camera = Picamera2()

        video_config = self.camera.create_video_configuration(main={"size": (1920, 1080)})
        self.camera.configure(video_config)
        self.camera.start()

        self.camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        # self.camera.set_controls({"AfTrigger": controls.AfTriggerEnum.Start})


    def process_image(self):
        while True:
            # Capture an image
            frame = self.camera.capture_array()
            hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            red_lower = np.array([136, 87, 111], np.uint8) 
            red_upper = np.array([180, 255, 255], np.uint8) 
            red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

            green_lower = np.array([25, 52, 72], np.uint8) 
            green_upper = np.array([102, 255, 255], np.uint8) 
            green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 

            

            blue_lower = np.array([94, 80, 2], np.uint8) 
            blue_upper = np.array([120, 255, 255], np.uint8) 
            blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper) 

            kernel = np.ones((5, 5), "uint8") 

            red_mask = cv2.dilate(red_mask, kernel) 
            res_red = cv2.bitwise_and(frame, frame, 
                                    mask = red_mask) 
            
            # For green color 
            green_mask = cv2.dilate(green_mask, kernel) 
            res_green = cv2.bitwise_and(frame, frame, 
                                        mask = green_mask) 
            
            # For blue color 
            blue_mask = cv2.dilate(blue_mask, kernel) 
            res_blue = cv2.bitwise_and(frame, frame, 
                                    mask = blue_mask) 

            # Creating contour to track red color 
            contours, hierarchy = cv2.findContours(red_mask, 
                                                cv2.RETR_TREE, 
                                                cv2.CHAIN_APPROX_SIMPLE) 
            
            for pic, contour in enumerate(contours): 
                area = cv2.contourArea(contour) 
                if(area > 500 and area < 6000): 
                    x, y, w, h = cv2.boundingRect(contour) 
                    frame = cv2.rectangle(frame, (x, y), 
                                            (x + w, y + h), 
                                            (0, 0, 255), 2) 
                    
                    cv2.putText(frame, "Red Colour", (x, y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                                (0, 0, 255))	 

            # Creating contour to track green color 
            contours, hierarchy = cv2.findContours(green_mask, 
                                                cv2.RETR_TREE, 
                                                cv2.CHAIN_APPROX_SIMPLE) 
            
            for pic, contour in enumerate(contours): 
                area = cv2.contourArea(contour) 
                if(area > 500 and area < 6000): 
                    x, y, w, h = cv2.boundingRect(contour) 
                    frame = cv2.rectangle(frame, (x, y), 
                                            (x + w, y + h), 
                                            (0, 255, 0), 2) 
                    
                    cv2.putText(frame, "Green Colour", (x, y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                1.0, (0, 255, 0)) 

            # Creating contour to track blue color 
            contours, hierarchy = cv2.findContours(blue_mask, 
                                                cv2.RETR_TREE, 
                                                cv2.CHAIN_APPROX_SIMPLE) 
            for pic, contour in enumerate(contours): 
                area = cv2.contourArea(contour) 
                if(area > 500 and area < 6000): 
                    x, y, w, h = cv2.boundingRect(contour) 
                    frame = cv2.rectangle(frame, (x, y), 
                                            (x + w, y + h), 
                                            (255, 0, 0), 2) 
                    
                    cv2.putText(frame, "Blue Colour", (x, y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                1.0, (255, 0, 0))

            # for name, color_bounds in colors.items():
            #     result = find_color(hsvFrame, color_bounds)
            #     if result:
            #         x, y, w, h = result

            #         cv2.rectangle(frame, (x,y), (x+w), (y+h), (0, 0, 255), 2)
            #         cv2.putText(frame, name, (x, y), 
			# 			cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
			# 			(0, 0, 255))
                    # c, cx, cy = result
                    # cv2.drawContours(frame, [c], -1, display_color, 3)
                    # cv2.circle(frame, (cx, cy), 7, display_color, -1)
                    # cv2.putText(frame, name, (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, display_color, 2)

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
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
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
