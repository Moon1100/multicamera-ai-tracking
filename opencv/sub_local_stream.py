import cv2
import requests
import numpy as np

# IP address of the video stream
video_url = 'http://192.168.0.108:8080/'

# Open the video stream using requests
stream = requests.get(video_url, stream=True)

# Create an empty byte buffer
byte_buffer = bytes()

for chunk in stream.iter_content(chunk_size=4096):
    byte_buffer += chunk
    a = byte_buffer.find(b'\xff\xd8')
    b = byte_buffer.find(b'\xff\xd9')
    if a != -1 and b != -1:
        # Found a complete frame
        frame_data = byte_buffer[a:b+2]
        byte_buffer = byte_buffer[b+2:]

        # Convert the frame data to a numpy array
        frame = np.frombuffer(frame_data, dtype=np.uint8)

        # Decode the frame
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        # Display the frame in a window
        cv2.imshow('Video Stream', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the OpenCV window
cv2.destroyAllWindows()
