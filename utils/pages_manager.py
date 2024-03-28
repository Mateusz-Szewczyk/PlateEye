import streamlit as st
from pathlib import Path
import json


def show_all_pages():
    st.sidebar.page_link("1_Main.py", label="Main Page")
    st.sidebar.page_link("pages/2_Add_Comment.py", label="Add Comment")
    st.sidebar.page_link("pages/3_My_Account.py", label="My Account")
