import sqlite3

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def get_user(conn, username, password):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return cur.fetchone()