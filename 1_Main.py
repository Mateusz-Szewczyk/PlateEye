import streamlit as st

from utils.login_and_register import log_and_reg
from utils.database_driver import get_last_number_plate_data
from utils.styling import default_style

st.set_page_config(page_title="PlateEye", page_icon="🚗", layout="wide")
default_style()
col1, col2 = st.columns(2)
with col1:
    st.title("PlateEye - Number Plate Detection and Recognition :car:")
with col2:
    with st.columns(3)[1]:
        st.image("./static/plateeye-logo.png", width=250)
log_and_reg()

data = get_last_number_plate_data(5)

for record in data:
    with st.container(border=True):
        col1, col2, col3 = st.columns(3, gap="medium")
        with st.container():
            with col1:
                with st.columns([1, 8, 1])[1]:
                    st.subheader(f"Added by: {record[0]}")
                    try:
                        st.image(f"{record[8]}", caption="Number Plate Image", width=300)
                    except:
                        st.image("./static/img-not-found.jpg", caption="Image not found")
        with st.container():
            if record[7] == "":
                with col2:
                    st.warning("No comment added")
            else:
                with col2:
                    with st.columns([1, 8, 2])[1]:
                        st.subheader("Comment")
                        st.write(f"{record[7]}")

        with st.container():
            with col3:
                st.subheader("Number Plate")
                st.write(f"{record[2]}")
    st.markdown("<br>", unsafe_allow_html=True)
