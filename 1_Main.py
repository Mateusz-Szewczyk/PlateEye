import streamlit as st
import streamlit_scrollable_textbox as stx

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
print(data)
for record in data:
    with st.container(border=True):
        col1, col2, col3 = st.columns(3, gap="medium")
        with st.container():
            with col1:
                with st.columns([1, 8, 1])[1]:
                    st.subheader(f"Added by: {record[0]}")
                    try:
                        st.image(f"{record[8]}", caption="Number Plate Image", height=300)
                    except:
                        st.image("./static/img-not-found.jpg", caption="Image not found")
        with st.container():
            with col2:
                with st.columns([1, 8, 2])[1]:
                    st.subheader("Comment")
                    if record[7] == "":
                        st.warning("No comment added")
                    else:
                        stx.scrollableTextbox(record[7], height=300, border=False)

        with st.container():
            with col3:
                st.subheader("Number Plate")
                st.write(f"{record[2]}")
    st.markdown("<br>", unsafe_allow_html=True)
