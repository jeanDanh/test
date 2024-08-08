import streamlit as st
import sqlite3
import pandas as pd

# Function to check if the user exists and the password is correct
def check_user(username, password):
    conn = sqlite3.connect('final1.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to create a new user
def create_user(username, password, email, full_name, role_id, current_user_role_id):
    allowed_roles = get_allowed_roles(current_user_role_id)
    if role_id not in allowed_roles:
        return False
    
    conn = sqlite3.connect('final1.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO User (username, password, email, full_name, role_id) VALUES (?, ?, ?, ?, ?)",
                       (username, password, email, full_name, role_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Function to get all roles and return a dictionary for easy lookup
def get_roles():
    conn = sqlite3.connect('final1.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Role")
    roles = cursor.fetchall()
    conn.close()
    # Create a dictionary from the list of tuples (role_id, role_name)
    return {role[1]: role[0] for role in roles}

# Function to get allowed roles based on current user's role
def get_allowed_roles(role_id):
    if role_id == 2:  # Teacher
        return {1}  # Can create only students
    elif role_id == 3:  # Admin
        return {1, 2}  # Can create students and teachers
    elif role_id == 4:  # Super Admin
        return {1, 2, 3, 4}  # Can create students, teachers, admins, and super admins
    else:
        return set()  # No roles can be created if not authorized

# Function to check if current role is allowed to create users
def can_create_users(role_id):
    return role_id in {2, 3, 4}  # teacher, admin, super admin

# Function to process the uploaded Excel file and create users
def process_excel(file, current_user_role_id):
    df = pd.read_excel(file)
    for _, row in df.iterrows():
        create_user(row['username'], row['password'], row['email'], row['full_name'], row['role_id'], current_user_role_id)


def main():
    st.title("Login")

    if 'logged_in_user' in st.session_state:
        user = st.session_state['logged_in_user']
        role_id = user[5]
        
        st.sidebar.title("Menu")
        if st.sidebar.button("Sign Out"):
            del st.session_state['logged_in_user']
            st.rerun()

        st.header("Welcome!")
        st.write(f"Full Name: {user[4]}")
        st.write(f"Email: {user[3]}")
        st.write(f"Role ID: {role_id}")

        # Display role-based content
        if role_id == 1:  # Student
            st.write("You are a student. Here is your dashboard.")
        elif role_id == 2:  # Teacher
            st.write("You are a teacher. Here are your classes.")
        elif role_id == 3:  # Admin
            st.write("You are an admin. Here is the admin panel.")
        elif role_id == 4:  # Super Admin
            st.write("You are a super admin. You have full control.")

        # Sign Up Form for Admins and Super Admins
        if can_create_users(role_id):
            st.header("Sign Up New User")
            roles_dict = get_roles()
            username = st.text_input("New Username")
            password = st.text_input("New Password", type='password')
            confirm_password = st.text_input("Confirm Password", type='password')
            email = st.text_input("Email")
            full_name = st.text_input("Full Name")
            role = st.selectbox("Role", list(roles_dict.keys()))
            role_id_to_create = roles_dict[role]

            if st.button("Create User"):
                if password != confirm_password:
                    st.error("Passwords do not match.")
                elif create_user(username, password, email, full_name, role_id_to_create, role_id):
                    st.success("User created successfully!")
                else:
                    st.error("User creation failed. Username or email might be taken or role is not allowed.")
            
            # Widget to upload Excel file and create users
            st.header("Import Users from Excel")
            excel_file = st.file_uploader("Upload Excel file", type=['xlsx'])
            if excel_file is not None:
                process_excel(excel_file, role_id)
                st.success("Users imported successfully!")
    else:
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            user = check_user(username, password)
            if user:
                st.session_state['logged_in_user'] = user
                st.rerun()
            else:
                st.error("Invalid username or password")

if __name__ == "__main__":
    main()