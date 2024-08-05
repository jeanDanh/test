import streamlit as st
import pandas as pd
import numpy as np
from auth import authenticate, create_new_user, create_connection

# Function to handle login
def login():
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_button = st.button("Login")

    if login_button:
        user = authenticate(username, password)
        if user:
            st.session_state.authenticated = True
            st.session_state.user = user
            st.success(f"Welcome, {user['username']}! You are logged in as a {user['role']}.")
        else:
            st.error("Invalid username or password")

# Function to handle user creation by teacher
def create_user():
    st.subheader("Create New User")
    new_username = st.text_input("New Username", key="new_username")
    new_password = st.text_input("New Password", type="password", key="new_password")
    new_role = st.selectbox("Role", ["student", "teacher"], key="new_role")
    create_user_button = st.button("Create User", key="create_user_button")

    if create_user_button:
        if new_username and new_password:
            create_new_user(new_username, new_password, new_role)
            st.success(f"User {new_username} created successfully!")
        else:
            st.error("Please fill out all fields to create a new user.")

# Function to handle bulk user creation from Excel file
def upload_excel():
    st.subheader("Upload Excel File")
    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.write(df)
        if st.button("Add Users from Excel"):
            conn = create_connection('users.db')
            for index, row in df.iterrows():
                create_new_user(row['username'], row['password'], row.get('role', 'student'))
            st.success("Users added successfully from the Excel file")

# Main function
def main():
    # Initialize session state variables if not already done
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None

    if st.session_state.authenticated:
        user = st.session_state.user
        st.success(f"Welcome, {user['username']}! You are logged in as a {user['role']}.")

        if user['role'] == 'student':
            st.write("Student content here...")
            df = pd.DataFrame({
                'first column': [1, 2, 3, 4],
                'second column': [10, 20, 30, 40]
            })
            st.write(df)

        elif user['role'] == 'teacher':
            st.write("Teacher content here...")

            dataframe = pd.DataFrame(
                np.random.randn(10, 20),
                columns=('col %d' % i for i in range(20))
            )
            st.dataframe(dataframe.style.highlight_max(axis=0))

            create_user()
            upload_excel()
    else:
        login()

if __name__ == "__main__":
    main()
