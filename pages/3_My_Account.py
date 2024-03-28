import streamlit as st

from utils.login_and_register import log_and_reg
from utils.login_and_register import save_config

st.set_page_config(page_title="My account", page_icon="🚗", layout="wide")
config, authenticator, name, authentication_status, username = log_and_reg()

st.title(f"Hey, *{name}*, here you can reset your password, or update user details :car:")
st.markdown('---')


if authenticator.reset_password(username, 'main'):
    save_config(config)
    st.success('Password modified successfully')


if authenticator.update_user_details(username, 'main'):
    save_config(config)
    st.success('Entries updated successfully')