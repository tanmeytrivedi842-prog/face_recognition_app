import face_recognition
import cv2
import numpy as np
import os
from utils.db import get_all_users


def load_known_faces():
    known_encodings = []
    known_names = []

    users = get_all_users()

    for user in users:
        name = user[1]
        image_path = user[2]

        if os.path.exists(image_path):
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)

            if encoding:
                known_encodings.append(encoding[0])
                known_names.append(name)

    return known_encodings, known_names


def recognize_faces(frame, known_encodings, known_names):

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    results = []

    for face_encoding, face_location in zip(face_encodings, face_locations):

        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_encodings, face_encoding)

        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_names[best_match_index]

        results.append((face_location, name))

    return results