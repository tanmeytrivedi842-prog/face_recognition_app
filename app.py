import streamlit as st
import cv2
import os
from utils.db import init_db, insert_user
from utils.face_utils import load_known_faces, recognize_faces

init_db()

st.title("Face Recognition System")

menu = ["Register Face", "Recognize Face"]
choice = st.sidebar.selectbox("Menu", menu)


# ---------------- REGISTER ---------------- #

if choice == "Register Face":

    st.subheader("Register New Face")

    name = st.text_input("Enter Name")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"])

    if uploaded_file and name:

        # Ensure images directory exists
        images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
            
        file_path = os.path.join(images_dir, f"{name}.jpg")

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        insert_user(name, file_path)

        st.success(f"{name} registered successfully!")


# ---------------- RECOGNITION ---------------- #

elif choice == "Recognize Face":

    st.subheader("Face Recognition")

    run = st.checkbox("Start Camera")

    if run:

        cap = cv2.VideoCapture(0)

        known_encodings, known_names = load_known_faces()

        FRAME_WINDOW = st.image([])

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            results = recognize_faces(frame, known_encodings, known_names)

            for (top, right, bottom, left), name in results:

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            FRAME_WINDOW.image(frame, channels="BGR")

        cap.release()