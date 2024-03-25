import streamlit as st
from anpr.detect_and_recognize import detect_number_plates, recognize_number_plates
import os
from ultralytics import YOLO
import time
import cv2
from easyocr import Reader


st.set_page_config(page_title="Number Plate Detection and Recognition", page_icon="🚗", layout="wide")

st.title("Number Plate Detection and Recognition :car:")
st.markdown("---")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
upload_path = "uploads"


if uploaded_file is not None:
    image_path = os.path.sep.join([upload_path, uploaded_file.name])
    with open(image_path, "wb") as file:
        file.write(uploaded_file.getbuffer())
    with st.spinner("In progress..."):
        model = YOLO("runs/detect/train/weights/best.pt")
        reader = Reader(["en"], gpu=True)
        image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        image_copy = image.copy()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(image)

        number_plate_list = detect_number_plates(image, model)
        if number_plate_list:
            number_plate_list = recognize_number_plates(image_path, reader, number_plate_list)
            for box, text in number_plate_list:
                cropped_number_plate = image_copy[box[1]:box[3], box[0]:box[2]]
                cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                cv2.putText(image, text, (box[0], box[3] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            with col2:
                st.subheader("Number Plate Detected Image")
                st.image(image)
            st.subheader("Cropped Number Plate")
            st.image(cropped_number_plate)
            st.success(f"Number plate: **{text}**, detected and recognized successfully!")
        else:
            st.error("No number plates detected in the image. Please try with another image.")
else:
    st.info("Please upload an image file to get started")