import streamlit as st
from pathlib import Path
import json



def show_all_pages():
    st.sidebar.page_link("1_Main.py", label="◼️ Main Page")
    st.sidebar.page_link("pages/2_📝_Add_Post.py", label="◼️ Add Post")
    st.sidebar.page_link("pages/3_🔧_My_Account.py", label="◼️ My Account")
