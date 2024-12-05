import streamlit as st
import cv2
import numpy as np
import face_recognition
from PIL import Image
import time


st.set_page_config(page_title="Face Recognition App", layout="wide")

st.title("🔍 Real-Time Face Recognition")
st.sidebar.title("Face Recognition Settings")
st.sidebar.subheader("Upload Images for Face Recognition")


uploaded_files = st.sidebar.file_uploader("Upload Image(s)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)


uploaded_face_encodings = []


def load_uploaded_image(uploaded_file):
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

    face_encodings = face_recognition.face_encodings(img_rgb)
    if len(face_encodings) > 0:
        return face_encodings[0] 
    return None


if uploaded_files:
    for uploaded_file in uploaded_files:
        uploaded_face_encoding = load_uploaded_image(uploaded_file)
        if uploaded_face_encoding is None:
            st.sidebar.error(f"❌ No face detected in {uploaded_file.name}. Please upload another image with a visible face.")
        else:
            uploaded_face_encodings.append(uploaded_face_encoding)
            st.sidebar.success(f"✅ Face uploaded from {uploaded_file.name} successfully!")


    st.header("Uploaded Image(s)")
    for uploaded_file in uploaded_files:
        st.image(uploaded_file, caption=f"Uploaded Image: {uploaded_file.name}", use_container_width=True)


st.header("Live Camera Feed")
stframe = st.empty()  
match_result = st.empty()  


cap = cv2.VideoCapture(0)  

last_match_time = None
match_duration = 10  #
face_matched = False

with st.spinner('Processing webcam feed...'):
    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("⚠️ Failed to grab frame from webcam.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
        
      
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        current_face_matched = False  

       
        if len(face_locations) == 0:
            match_result.text("❌ No face detected!")
            match_result.markdown("<h3 style='color: orange;'>❌ No face detected!</h3>", unsafe_allow_html=True)
        else:
            
            for face_encoding in face_encodings:
                for uploaded_face_encoding in uploaded_face_encodings:
                   
                    matches = face_recognition.compare_faces([uploaded_face_encoding], face_encoding)
                    face_distances = face_recognition.face_distance([uploaded_face_encoding], face_encoding)

                    
                    if True in matches and min(face_distances) < 0.4:
                        current_face_matched = True
                        break

            
            if current_face_matched:
                if not face_matched:
                    last_match_time = time.time()  
                face_matched = True
                match_result.text("✅ Matched!")
                match_result.markdown("<h3 style='color: green;'>✅ Face Matched!</h3>", unsafe_allow_html=True)
            else:
                if face_matched:
                   
                    if time.time() - last_match_time >= match_duration:
                        face_matched = False
                        match_result.text("❌ Face Mismatched!")
                        match_result.markdown("<h3 style='color: red;'>❌ Face Mismatched!</h3>", unsafe_allow_html=True)
                else:
                    match_result.text("❌ Face Mismatched!")
                    match_result.markdown("<h3 style='color: red;'>❌ Face Mismatched!</h3>", unsafe_allow_html=True)

          
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

       
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (640, 480))

        
        stframe.image(frame_resized, channels="RGB", use_container_width=False)

        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
