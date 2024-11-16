import cv2
import numpy as np

def empty(a):
    pass

def detect_rectangles(frame, threshold1, threshold2):
    """
    Detects rectangles in the given frame using Canny edge detection and contour analysis.

    Args:
        frame: The input frame from the webcam.
        threshold1: Lower threshold for the Canny edge detector.
        threshold2: Upper threshold for the Canny edge detector.

    Returns:
        Processed frame with detected rectangles drawn.
    """
    # Apply GaussianBlur to reduce noise and improve edge detection
    blurred = cv2.GaussianBlur(frame, (7, 7), 1)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    # Apply Canny Edge Detection
    edges = cv2.Canny(gray, threshold1, threshold2)

    # Find contours from the edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            cv2.drawContours(frame, contour, -1, (255, 0, 255), 7)
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            x_, y_, w_, l_ = cv2.boundingRect(approx)
            cv2.rectangle(frame, (x_, y_), (x_ + w_, y_ + l_), (0, 255, 0), 5)

    return frame

def main():
    # Capture video from the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Get the threshold values from the trackbars
        threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
        threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")

        # Detect rectangles in the frame
        processed_frame = detect_rectangles(frame, threshold1, threshold2)

        # Display the processed frame
        cv2.imshow("Rectangle Detection", processed_frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Create a named window for the trackbars and output
    cv2.namedWindow("Parameters")
    cv2.createTrackbar("Threshold1", "Parameters", 50, 255, empty)
    cv2.createTrackbar("Threshold2", "Parameters", 150, 255, empty)

    # Start the main loop
    main()
