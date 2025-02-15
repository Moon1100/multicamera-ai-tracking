import cv2
from flask import Flask, Response
import socket
import face_recognition
import os


app = Flask(__name__)

def generate_frames():
    video_capture = cv2.VideoCapture(0)
    # get frame rate
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    print("Frame rate:", fps)

    # get resolution
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    width_center = width//2
    height_center = height//2

    # print("Resolution:", width, "x", height)

    # Get the filename of the first JPG file in the storage folder
    jpg_files = [f for f in os.listdir("storage") if f.endswith(".jpg")]
    if jpg_files:
        target_image_filename_only, _ = os.path.splitext(jpg_files[0])
        target_image_filename = jpg_files[0]

        target_image_path = os.path.join("storage", target_image_filename)
    else:
        flash('No target initialized', 'error')

    # Load a sample picture and learn how to recognize it.
    target_image = face_recognition.load_image_file(target_image_path)
    target_face_encoding = face_recognition.face_encodings(target_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        target_face_encoding
    ]
    known_face_names = [
        target_image_filename_only,
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # # Process the frame
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        horizontal_offset = 'und'
        vertical_offset = 'und'
        font = cv2.FONT_HERSHEY_DUPLEX


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # faces = frame[top:bottom, left:right]

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)

            # Center coordinates
            forhead_coordinates = (((right-left)//2+left), top)
            center_coordinates = (((right-left)//2+left), (bottom-top)//2+top)

            # Radius of circle
            radius = 5

            # Blue color in BGR
            color = (255, 0, 0)

            # Line thickness of 2 px
            thickness = 2

            # Draw a box center the face
            cv2.circle(frame, forhead_coordinates, radius, color, thickness)

            # draw camera center
            start_point_verticle = (width_center, 0)

            # End coordinate, here (250, 250)
            # represents the bottom right corner of image
            end_point_horizontal = (width_center, height)

            # Green color in BGR
            color = (0, 255, 0)

            # Line thickness of 9 px
            thickness = 1

            # Draw a vertical green line with thickness of 9 px
            cv2.line(frame, start_point_verticle,
                     end_point_horizontal, color, thickness)

            start_point_horizontal = (0, height_center)
            end_point_horizontal = (width, height_center)
            # Draw a horizontal green line with thickness of 9 px
            cv2.line(frame, start_point_horizontal,
                     end_point_horizontal, color, thickness)

            # print("horizontal offset : "+str(height/2-center_coordinates[1]))
            # print("vertical offset : "+str(width/2-center_coordinates[0]))

            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)
            horizontal_offset = (width/2 - center_coordinates[1])
            vertical_offset = (height/2 -
                               center_coordinates[0])

        cv2.putText(frame, "y :"+str(horizontal_offset),
                    (1020, 600), font, 1.0, (255, 255, 255), 1)
        cv2.putText(frame, "x :"+str(vertical_offset),
                    (1020, 630), font, 1.0, (255, 255, 255), 1)
        

        #publish the offset to camera for correction
        message = str([vertical_offset,horizontal_offset])
        
       

  

        # Convert the processed frame to a byte stream
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        # Get the IP address dynamically
        address = socket.gethostbyname(socket.gethostname())
        port = 8080  # Replace with your desired port number
        ip_address = f"{address}:{port}"

    except socket.gaierror:
        # Fallback option if hostname resolution fails
        ipAddress = '0.0.0.0'

    # Run the app
    app.run(host=ipAddress, port=8080, debug=True)
