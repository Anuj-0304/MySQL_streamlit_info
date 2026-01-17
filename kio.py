import streamlit as st
import mysql.connector
import bcrypt
import pandas as pd
import numpy as np
import base64
from PIL import Image

# -------------------------------------------------
# PAGE CONFIG (ONLY ONCE, AT TOP)
# -------------------------------------------------
st.set_page_config(
    page_title="Krishi Saarthi",
    layout="wide"
)

# -------------------------------------------------
# DATABASE & AUTH
# -------------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Anuj#2006",   # must match mysql -u root -p
        database="krishi_saarthi",
        auth_plugin="mysql_native_password"
    )

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, hash_password(password))
    )
    conn.commit()
    cursor.close()
    conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password FROM users WHERE username=%s",
        (username,)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return verify_password(password, result[0])
    return False

# -------------------------------------------------
# LOGIN / SIGNUP PAGE
# -------------------------------------------------
def login_page():
    st.title("🌱 Krishi Saarthi")
    st.subheader("Login / Sign Up")

    choice = st.radio("Select option", ["Login", "Sign Up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Sign Up":
        if st.button("Create Account"):
            if not username or not password:
                st.warning("Username and password cannot be empty")
            else:
                try:
                    register_user(username, password)
                    st.success("Account created successfully. Please login.")
                except Exception as e:
                    st.error(e)

    else:
        if st.button("Login"):
            if login_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["user"] = username
                st.rerun()
            else:
                st.error("Invalid username or password")

# -------------------------------------------------
# MAIN WEBSITE (YOUR EXISTING CODE)
# -------------------------------------------------
def main_app():
    # Logo
    img = Image.open("website_logo.jpg")
    st.image(img, width=200)

    # Background color
    st.markdown("""
        <style>
        .stApp { background-color: #dedbd2; }
        </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown(
        "<h1 style='text-align:center; font-size:80px;'>Krishi Saarthi</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<hr style='height:3px; background-color:#2c6e49;'>",
        unsafe_allow_html=True
    )

    # -------------------------------------------------
    # GOVERNMENT SCHEMES SCROLL
    # -------------------------------------------------
    def img_to_base64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    images_with_links = [
        ("img1.jpg", "https://pmkisan.gov.in/"),
        ("img2.jpg", "https://pmfby.gov.in/"),
        ("img3.jpg", "https://pmksy.gov.in/")
    ]

    html = "<div style='display:flex;overflow-x:auto;gap:16px;'>"
    for img, link in images_with_links:
        html += f"""
        <a href="{link}" target="_blank">
            <img src="data:image/jpeg;base64,{img_to_base64(img)}"
            style="width:700px;height:250px;border-radius:12px;">
        </a>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

    st.markdown(
        "<hr style='height:3px; background-color:#2c6e49;'>",
        unsafe_allow_html=True
    )

    # -------------------------------------------------
    # FEATURE CARDS
    # -------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("Know More About Weather Prediction"):
            st.write(
                "Weather prediction helps farmers take informed decisions "
                "about irrigation, sowing, and harvesting."
            )
        st.markdown(
            "[Weather Prediction App](https://weather-prediction-bu7p6nawxu45huhizjyedx.streamlit.app/)"
        )

    with col2:
        with st.expander("Know More About Crop Disease Detection"):
            st.write(
                "AI-based crop disease detection helps identify plant diseases early."
            )
        st.markdown(
            "[AI Saarthi](https://crop-disease-detection-r4kvmjzyew58ewgktelgxh.streamlit.app/)"
        )

    st.markdown(
        "<hr style='height:3px; background-color:#2c6e49;'>",
        unsafe_allow_html=True
    )

    st.subheader("Crop Care / Maintenance Advisory")
    st.markdown(
        "[Open Advisory](https://aiadvisory-rtmavckgcc5tbzr4nqzunu.streamlit.app/)"
    )

    # Logout
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# -------------------------------------------------
# APP ENTRY POINT
# -------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    login_page()
