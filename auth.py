from db import create_connection, get_user

def authenticate(username, password):
    conn = create_connection('users.db')
    user = get_user(conn, username, password)
    conn.close()
    if user:
        return {"username": user[1], "role": user[3]}
    else:
        return None