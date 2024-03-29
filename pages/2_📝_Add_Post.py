import os
import cv2
import streamlit as st

from utils.anpr import detect_number_plates, recognize_number_plates, model_and_reader
from utils.image_processing import prepare_images
from utils.saving import create_image_dir
from utils.database_driver import add_post
from utils.login_and_register import log_and_reg
from utils.styling import default_style

st.set_page_config(page_title="Add Comment", page_icon="📝", layout="wide")
st.title("PlateEye - Number Plate Detection and Recognition :car:")
default_style()
config, authenticator, name, authentication_status, username = log_and_reg()

st.markdown("---")
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

st.session_state['post_added'] = None
if st.session_state['post_added'] is None:
    st.session_state['post_added'] = False

if not st.session_state['post_added']:
    if uploaded_file is not None:
        image_dir, image_path = create_image_dir(uploaded_file, username)

        with st.spinner("In progress..."):
            model, reader = model_and_reader()
            image, image_copy = prepare_images(image_path)
            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("Original Image")
                st.image(image)

            bounding_boxes_list = detect_number_plates(image, model)
            if bounding_boxes_list:
                with col2:
                    st.subheader("Number Plate Detected Image")
                    st.image(image)
                bbox_and_number_plate_list, number_plates_img_list = recognize_number_plates(image_path, reader, bounding_boxes_list)
                with col3:
                    st.subheader("Processed Image")
                    for i in range(min(4, len(number_plates_img_list))):
                        st.image(number_plates_img_list[i])
                for i, (box, text) in enumerate(bbox_and_number_plate_list):
                    box = box
                    text = text
                    cropped_number_plate = image_copy[box[1]:box[3], box[0]:box[2]]
                    cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                    cv2.putText(image, text, (box[0], box[3] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    st.subheader("Cropped Number Plate")
                    st.image(cropped_number_plate)
                    st.success(f"Number plate: **{text}**, detected and recognized successfully!")
                    # Save the cropped number plate with the text as the filename
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    image_text_path = os.path.join(image_dir, f"{text}.{uploaded_file.name.split('.')[1]}")
                    cv2.imwrite(image_text_path, image)

                uploaded_file = None
                with st.form("add_number_plate_data"):
                    st.session_state['post_added'] = True
                    date = image_path.split(".")[0]
                    number_plate = st.text_input("Enter the naumber plate", value=text)
                    content = st.text_area("Add a comment")
                    if st.form_submit_button("Post"):
                        add_post(username, content, box, number_plate, image_text_path, date)
                        st.success("Number plate data added successfully!")
            else:
                st.error("No number plates detected in the image. Please try with another image.")
    else:
        st.info("Please upload an image file to get started")
else:
    if st.button("Do you want to try with another image?"):
        st.session_state['post_added'] = False
        st.experimental_rerun()
