import streamlit as st

from utils.login_and_register import log_and_reg

st.set_page_config(page_title="PlateEye", page_icon="🚗", layout="wide")
st.title("PlateEye - Number Plate Detection and Recognition :car:")
log_and_reg()


for i in range(10):
    st.subheader(f"Header {i}")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Column 1")
    with col2:
        st.write("Column 2")
    with col3:
        st.write("Column 3")