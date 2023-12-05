import socket
import cv2
from flask import Flask, Response
import threading

app = Flask(__name__)

class VideoStreamThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.video_capture = cv2.VideoCapture(0)
        self.frame_available = threading.Event()
        self.frame = None
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            ret, frame = self.video_capture.read()
            if not ret:
                break
            self.frame = frame
            self.frame_available.set()
            self.frame_available.clear()

    def stop(self):
        self.running = False
        self.video_capture.release()

    def get_frame(self):
        self.frame_available.wait()
        return self.frame


@app.route('/')
def stream():
    def generate_frames():
        while True:
            frame = video_stream.get_frame()
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()

            yield (b'--boundarydonotcross\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=boundarydonotcross')


if __name__ == '__main__':
    try:
        # Get the IP address dynamically
        address = socket.gethostbyname(socket.gethostname())
        port = 8080  # Replace with your desired port number
        ip_address = "{}:{}".format(address, port)

    except socket.gaierror:
        # Fallback option if hostname resolution fails
        ip_address = '0.0.0.0'

    video_stream = VideoStreamThread()
    video_stream.start()

    # Run the app
    app.run(host=ip_address, port=8080, debug=True)

    # Stop the video stream thread
    video_stream.stop()
    video_stream.join()
