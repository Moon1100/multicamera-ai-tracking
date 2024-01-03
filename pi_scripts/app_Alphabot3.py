import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# Initialize the PiCamera
camera = PiCamera()

# Set camera resolution (you can adjust these values based on your preferences)
camera.resolution = (640, 480)
camera.framerate = 30

# Allow the camera to warm up
time.sleep(2)

# Create an OpenCV video capture object
raw_capture = PiRGBArray(camera, size=camera.resolution)

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# Capture frames from the camera
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    # Get the NumPy array representing the image
    image = frame.array

    # Display the image (optional)
    cv2.imshow("Frame", image)

    # Write the frame to the video file
    out.write(image)

    # Clear the stream in preparation for the next frame
    raw_capture.truncate(0)

    # Break the loop if 'q' key is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Release the video writer and close OpenCV windows
out.release()
cv2.destroyAllWindows()
