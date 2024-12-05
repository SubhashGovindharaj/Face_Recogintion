# 🔍 Real-Time Face Recognition App

This **Real-Time Face Recognition App** leverages OpenCV and the `face_recognition` library to recognize faces in real-time from a live camera feed. Users can upload reference images, and the app will compare the live camera feed against these images to detect and verify face matches.

---

## Features
- 📷 **Live Camera Feed**: Detect faces in real-time using a webcam.
- 🖼️ **Image Uploads**: Upload one or more images for face recognition comparison.
- ✅ **Real-Time Matching**: Matches live camera faces with uploaded reference faces.
- 🚨 **Mismatch Alerts**: Provides real-time alerts when faces don't match or aren't detected.
- 🖥️ **Interactive Interface**: Built with Streamlit for a seamless user experience.

---

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- A webcam connected to your system
- Required Python libraries (listed in `requirements.txt`)

### Installation Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SubhashGovindharaj/Face_Recogintion.git
   cd Face_Recogintion

Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Run the Application:

bash
Copy code
streamlit run app.py
