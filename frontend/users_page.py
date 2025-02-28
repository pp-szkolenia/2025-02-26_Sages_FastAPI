import streamlit as st
import pandas as pd

# Mock data


def users_page(users):
    st.header("Manage Users")

    # Display users
    df_users = pd.DataFrame(users)
    st.write("### Existing Users")
    st.dataframe(df_users)

    # Add new user
    with st.form("new_user_form"):
        st.subheader("Add New User")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        is_admin = st.checkbox("Is Admin")
        submit_user = st.form_submit_button("Add User")

        if submit_user:
            new_user = {"id": len(users) + 1, "username": username, "password": password,
                        "is_admin": is_admin}
            users.append(new_user)
            st.success("User added successfully!")
            # API CALL: POST /users (send new_user)

    # Delete user
    delete_user_id = st.number_input("Enter User ID to delete", min_value=1, step=1)
    if st.button("Delete User"):
        users = [user for user in users if user["id"] != delete_user_id]
        st.success(f"User {delete_user_id} deleted successfully!")
        # API CALL: DELETE /users/{delete_user_id}
