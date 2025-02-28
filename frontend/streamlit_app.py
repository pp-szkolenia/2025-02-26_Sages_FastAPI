import streamlit as st
import pandas as pd
from tasks_page import tasks_page
from users_page import users_page
from login_page import login_page


st.title("Task Management Dashboard")

# Sidebar navigation
menu = st.sidebar.selectbox("Choose an option", ["Login", "Tasks", "Users"])

users = [
    {"id": 1, "username": "admin", "password": "admin123", "is_admin": True},
    {"id": 2, "username": "user1", "password": "userpass", "is_admin": False},
]

tasks = [
    {"id": 1, "description": "Task 1", "priority": 1, "is_completed": False},
    {"id": 2, "description": "Task 2", "priority": 2, "is_completed": True},
]


if menu == "Tasks":
    tasks_page(tasks)
elif menu == "Users":
    users_page(users)
elif menu == "Login":
    login_page()