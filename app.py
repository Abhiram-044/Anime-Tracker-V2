import streamlit as st
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from menu import menu_with_redirect

def init_db():
    conn = st.connection("mysql", "sql")
    with conn.session as s:
        s.execute('''CREATE TABLE IF NOT EXISTS Users (user_id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL);''')
        s.commit()
    return conn

def authenticate_user(username, password, conn):
    query = text("SELECT * FROM Users WHERE name = :username;")
    with conn.session as s:
        data = s.execute(query, {"username": username})
    user_data = data.fetchone()
    if user_data and user_data[2] == password:
        
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.success("Login Successful.")
        st.rerun()
    else:
        st.error("Invalid username or password")

def register_user(username, password, conn):
    query = "INSERT INTO Users (name, password) VALUES (:username, :password)"
    query2 = f'''CREATE TABLE {username} (
    anime_id INT PRIMARY KEY AUTO_INCREMENT,
    image_link VARCHAR(255),
    title VARCHAR(255) UNIQUE NOT NULL,
    rating TINYINT UNSIGNED CHECK (rating >= 0 AND rating <= 10),
    status VARCHAR(30)
    );'''
    try:
        with conn.session as s:
            s.execute(query, {"username": username, "password": password})
            s.execute(query2)
            s.commit()
        st.success("Registration Successful. Please Login.")
    except IntegrityError:
        st.error("Username already exists. Please choose a diffrent username.")

def login_page(conn):
    st.title("Welcome to Anime-Tracker")

    username_input = st.text_input("User: ")
    password_input = st.text_input("Password: ", type="password")

    cols = st.columns(2)
    if cols[0].button("Login", key="Login"):
        authenticate_user(username_input, password_input, conn)
    if cols[1].button("Register", key="Register"):
        register_user(username_input, password_input, conn)

def main():
    conn = init_db()
    
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    menu_with_redirect()
    if st.session_state["logged_in"]:
        st.title(f"Welcome, {st.session_state.get('username')}")
        
    else:
        login_page(conn)

if __name__ == "__main__":
    main()