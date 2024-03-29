import streamlit as st

from utils.login_and_register import log_and_reg
from utils.database_driver import get_last_number_plate_data

st.set_page_config(page_title="PlateEye", page_icon="🚗", layout="wide")
st.title("PlateEye - Number Plate Detection and Recognition :car:")
log_and_reg()

data = get_last_number_plate_data(5)

print(data)
for record in data:
    st.subheader(f"Added by: {record[0]}")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(f"{record[8]}", caption="Number Plate Image")
    with col2:
        st.subheader("Comment")
        st.write(f"{record[7]}")
    with col3:
        st.write("Number plate: ", f"{record[2]}")