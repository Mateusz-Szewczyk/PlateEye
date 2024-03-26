import os
import cv2
import streamlit as st

from utils.anpr import detect_number_plates, recognize_number_plates, model
from utils.image_processing import prepare_images
from utils.saving import create_image_dir

st.set_page_config(page_title="PlateEye", page_icon="🚗", layout="wide")
st.title("PlateEye - Number Plate Detection and Recognition :car:")
st.markdown("---")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image_dir = create_image_dir(uploaded_file)

    with st.spinner("In progress..."):
        model = model()
        image, image_copy = prepare_images(uploaded_file, image_dir)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Original Image")
            st.image(image)

        bounding_boxes_list = detect_number_plates(image, model)
        if bounding_boxes_list:
            with col2:
                st.subheader("Number Plate Detected Image")
                st.image(image)
            bbox_and_number_plate_list, number_plates_img_list = recognize_number_plates(os.path.join(image_dir, uploaded_file.name), bounding_boxes_list)
            with col3:
                st.subheader("Processed Image")
                for i in range(min(4, len(number_plates_img_list))):
                    st.image(number_plates_img_list[i])
            for i, (box, text) in enumerate(bbox_and_number_plate_list):
                cropped_number_plate = image_copy[box[1]:box[3], box[0]:box[2]]
                cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                cv2.putText(image, text, (box[0], box[3] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                st.subheader("Cropped Number Plate")
                st.image(cropped_number_plate)
                st.success(f"Number plate: **{text}**, detected and recognized successfully!")
                # Save the cropped number plate with the text as the filename
                # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                cv2.imwrite(os.path.join(image_dir, f"text_{text}.{uploaded_file.name.split('.')[1]}"), cropped_number_plate)
        else:
            st.error("No number plates detected in the image. Please try with another image.")
else:
    st.info("Please upload an image file to get started")
