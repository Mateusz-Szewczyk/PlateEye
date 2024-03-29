import yaml
from yaml.loader import SafeLoader
import smtplib
from pathlib import Path
from email.message import EmailMessage

import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher

from utils.pages_manager import show_all_pages

yaml_file = 'utils/auth.yaml'

# TODO Prevent logging out after refreshing the page

def save_config(config):
    try:
        with open(yaml_file, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(f"Error saving configuration: {e}")


def load_config():
    try:
        with open(yaml_file) as file:
            return yaml.load(file, Loader=SafeLoader)
    except Exception as e:
        st.error(f"Error loading configuration: {e}")
        return {}


def is_bcrypt_hash(s):
    bcrypt_prefixes = ('$2a$', '$2b$', '$2x$', '$2y$')
    return any(s.startswith(prefix) and len(s) == 60 for prefix in bcrypt_prefixes)



def send_email(subject, body, to_email, config):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = config['smtp']['username']
    msg['To'] = to_email

    with smtplib.SMTP(config['smtp']['server'], config['smtp']['port']) as server:
        if config['smtp']['use_tls']:
            server.starttls()
        server.login(config['smtp']['username'], config['smtp']['password'])
        server.send_message(msg)


def send_reset_password_email(name, new_password, to_email, config):
    subject = "Your New Password"
    body = f"Hey {name},\n\nHere is your new password:\n\n {new_password}\n\nPlease change it once you log in."

    send_email(subject, body, to_email, config)


def send_forgot_username_email(name, username, to_email, config):
    subject = "Your Username Reminder"
    body = f"Hey {name},\n\nYour username is: \n\n{username}\n\n"

    send_email(subject, body, to_email, config)


def hash_plaintext_passwords(config):
    plaintext_passwords = {}
    for user, details in config['credentials']['usernames'].items():
        # Check if the password is not a bcrypt hash
        if not is_bcrypt_hash(details['password']):
            plaintext_passwords[user] = details['password']

    if plaintext_passwords:
        hashed_passwords = stauth.utilities.hasher.Hasher(list(plaintext_passwords.values())).generate()
        for user, hashed_pw in zip(plaintext_passwords.keys(), hashed_passwords):
            config['credentials']['usernames'][user]['password'] = hashed_pw

    return config


def log_and_reg():
    config = load_config()
    st.session_state.setdefault('failed_login_attempts', 0)
    st.session_state['welcome_message'] = True
    if 'hashed_done' not in st.session_state:
        config = hash_plaintext_passwords(config)
        save_config(config)
        st.session_state.hashed_done = True

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    if st.session_state.get('authentication_status') is None:
        st.sidebar.page_link("1_Main.py", label="◼️ Main Page")
    name, authentication_status, username = authenticator.login('sidebar')
    if authentication_status:
        show_all_pages()
        st.sidebar.markdown('---')
        # If the user is authenticated
        if st.session_state['welcome_message']:
            st.sidebar.success(f'\n\nLogged in as, *{name}*')
            st.sidebar.markdown('---')
            st.session_state.welcome_message = False
        authenticator.logout('Logout', 'sidebar', key='unique_key')
        st.session_state.failed_login_attempts = 0
    else:
        if st.session_state.get("authentication_status") is False:
            st.session_state.failed_login_attempts += 1
            st.sidebar.error('Username/password is incorrect')

        # Register User
        try:
            if authenticator.register_user('sidebar', pre_authorization=False):
                save_config(config)
                if st.session_state['authentication_status']:
                    st.sidebar.success('User registered successfully')
        except Exception as e:
            st.error(str(e))

        st.markdown('---')

        # Forgot Password
        if st.session_state.failed_login_attempts >= 1:
            try:
                username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('sidebar')
                if username_forgot_pw:
                    user_name = config['credentials']['usernames'][username_forgot_pw][
                        'name']  # Assuming you store the name in the config
                    save_config(config)
                    # Send the reset password email
                    send_reset_password_email(user_name, random_password, email_forgot_password, config)
                    st.sidebar.success('New password sent securely')
                else:
                    if st.session_state.failed_login_attempts >= 1:
                        st.sidebar.error('Username not found')
            except Exception as e:
                st.sidebar.error(str(e))

    # Forgot Username
        if st.session_state.failed_login_attempts >= 1:
            try:
                username_forgot_username, email_forgot_username = authenticator.forgot_username('sidebar')
                if username_forgot_username:
                    user_name = config['credentials']['usernames'][username_forgot_username]['name']  # Retrieve the user's name from the config
                    save_config(config)
                    # Send the email with the username
                    send_forgot_username_email(user_name, username_forgot_username, email_forgot_username, config)
                    st.sidebar.success('Username sent securely')
                else:
                    st.sidebar.error('Email not found')
            except Exception as e:
                st.error(str(e))

    return config, authenticator, name, authentication_status, username



# TODO wyslij email potwierdzajacy rejestracje