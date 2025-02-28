import streamlit as st
import pandas as pd

# Mock user data
users = [
    {"id": 1, "username": "admin", "password": "admin123", "is_admin": True},
    {"id": 2, "username": "user1", "password": "userpass", "is_admin": False},
]

logged_in_user = None


def login_page():
    global logged_in_user
    st.header("Login Panel")

    if logged_in_user:
        st.success(f"Logged in as {logged_in_user['username']}")
        if st.button("Logout"):
            logged_in_user = None
            st.rerun()
        update_user_info()
    else:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        if login_button:
            for user in users:
                if user["username"] == username and user["password"] == password:
                    logged_in_user = user
                    st.success(f"Welcome {username}!")
                    st.rerun()
            st.error("Invalid username or password")


def update_user_info():
    global logged_in_user
    if logged_in_user:
        st.subheader("Update Your Information")

        if logged_in_user["is_admin"]:
            user_id = st.number_input("Enter User ID to update", min_value=1, step=1)
            selected_user = next((user for user in users if user["id"] == user_id), None)
        else:
            selected_user = logged_in_user

        if selected_user:
            new_username = st.text_input("New Username", value=selected_user["username"])
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Current Password", type="password")

            if st.button("Update"):
                if confirm_password == selected_user["password"]:
                    selected_user["username"] = new_username
                    selected_user["password"] = new_password
                    st.success("User information updated successfully!")
                    # API CALL: PUT /users/{selected_user['id']} (update username and password)
                else:
                    st.error("Incorrect current password!")
