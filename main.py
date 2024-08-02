import streamlit as st
import pandas as pd
import numpy as np
from auth import authenticate

def main():
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        user = authenticate(username, password)
        if user:
            st.success(f"Welcome, {user['username']}! You are logged in as a {user['role']}.")
            if user['role'] == 'student':
                
                st.write("Student content here...")
               
                df = pd.DataFrame({
                'first column': [1, 2, 3, 4],
                'second column': [10, 20, 30, 40]
                })

                df

            elif user['role'] == 'teacher':
                st.write("Teacher content here...")

                dataframe = pd.DataFrame(
                np.random.randn(10, 20),
                columns=('col %d' % i for i in range(20)))

                st.dataframe(dataframe.style.highlight_max(axis=0))
        else:
            st.error("Invalid username or password")

if __name__ == "__main__":
    main()