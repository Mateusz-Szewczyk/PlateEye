import streamlit as st
from ultralytics import YOLO
import cv2
from easyocr import Reader
import os
from detect_and_recognize import detect_number_plates, recognize_number_plates

st.set_page_config(page_title="Number Plate Detection and Recognition", page_icon="🚗", layout="wide")
st.title("Number Plate Detection and Recognition :car:")
st.markdown("---")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    uploaded_file_data = "uploaded-file-data"
    upload_image_path = os.path.join(uploaded_file_data, "uploads")
    csv_path = os.path.join(uploaded_file_data, "number_plates.csv")
    image_dir = os.path.join(upload_image_path, uploaded_file.name.split(".")[0])
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    if not os.path.exists(upload_image_path):
        os.makedirs(upload_image_path)
    with open(os.path.join(image_dir, uploaded_file.name, ), "wb") as file:
        file.write(uploaded_file.getbuffer())

    with st.spinner("In progress..."):
        model = YOLO("runs/detect/train/weights/best.pt")
        reader = Reader(["en"], gpu=True)
        image = cv2.cvtColor(cv2.imread(os.path.join(image_dir, uploaded_file.name)), cv2.COLOR_BGR2RGB)
        image_copy = image.copy()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(image)

        number_plate_list = detect_number_plates(image, model)
        if number_plate_list:
            with col2:
                st.subheader("Number Plate Detected Image")
                st.image(image)
            number_plate_list = recognize_number_plates(os.path.join(image_dir, uploaded_file.name), reader, number_plate_list)
            for i, (box, text) in enumerate(number_plate_list):
                cropped_number_plate = image_copy[box[1]:box[3], box[0]:box[2]]
                cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                cv2.putText(image, text, (box[0], box[3] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                st.subheader("Cropped Number Plate")
                st.image(cropped_number_plate)
                st.success(f"Number plate: **{text}**, detected and recognized successfully!")
                # Save the cropped number plate with the text as the filename
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                cv2.imwrite(os.path.join(image_dir, f"text_{text}.{uploaded_file.name.split('.')[1]}"), cropped_number_plate)
        else:
            st.error("No number plates detected in the image. Please try with another image.")
else:
    st.info("Please upload an image file to get started")
