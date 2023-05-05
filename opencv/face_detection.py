import face_recognition
import cv2
import numpy as np



def detect_face(cv2):
    video_capture = cv2.VideoCapture(0)
    # get frame rate
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    print("Frame rate:", fps)

    # get resolution
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    width_center=width_center
    height_center=height_center

    print("Resolution:", width, "x", height)

    # Load a sample picture and learn how to recognize it.
    obama_image = face_recognition.load_image_file("aliff.jpg")
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

    # Load a second sample picture and learn how to recognize it.
    biden_image = face_recognition.load_image_file("biden.jpg")
    biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        obama_face_encoding,
        biden_face_encoding
    ]
    known_face_names = [
        "aliff",
        "Joe Biden"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)


            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

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



            #draw camera center
            start_point_verticle = (width_center, 0)
    
            # End coordinate, here (250, 250)
            # represents the bottom right corner of image
            end_point_horizontal = (width_center, height)
            
            # Green color in BGR
            color = (0, 255, 0)
            
            # Line thickness of 9 px
            thickness = 1
            
            # Draw a vertical green line with thickness of 9 px
            cv2.line(frame, start_point_verticle, end_point_horizontal, color, thickness)

            start_point_horizontal = (0, height_center)
            end_point_horizontal = (width, height_center)
            # Draw a horizontal green line with thickness of 9 px
            cv2.line(frame, start_point_horizontal, end_point_horizontal, color, thickness)

            print("horizontal offset : "+str(height/2-center_coordinates[1]))
            print("vertical offset : "+str(width/2-center_coordinates[0]))

            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()