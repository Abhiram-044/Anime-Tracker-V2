import streamlit as st
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

def add_anime(anime):
    rating = st.session_state.get(f"rating_{anime['id']}")
    status = st.session_state.get(f"status_{anime['id']}")
    username = st.session_state.get("username")
    conn = st.connection("mysql", "sql")

    try:
        sql_statement = f'''INSERT INTO {username} (image_link, title, rating, status) VALUES (:anime_image, :anime_title, :user_rating, :user_status);'''
        with conn.session as s:
            s.execute(sql_statement, {"anime_image": anime["image"], "anime_title": anime["title"], "user_rating": rating, "user_status": status})
            s.commit()
        st.success("Added Succesfully. ")
    except IntegrityError:
        sql_statement = f'''UPDATE {username} SET rating = :user_rating, status = :user_status WHERE title = :anime_title;'''
        with conn.session as s:
            s.execute(sql_statement, {"user_rating": rating, "user_status": status, "anime_title": anime['title']})
            s.commit()
        st.success("Updated Show Successfully")


def update_anime(anime, id):
    rating = st.session_state.get(f"rating_{id}")
    status = st.session_state.get(f"status_{id}")
    username = st.session_state.get("username")
    conn = st.connection("mysql", "sql")

    sql_statement = f'''UPDATE {username} SET rating = :user_rating, status = :anime_status WHERE title = :anime_title;'''
    with conn.session as s:
        s.execute(sql_statement, {"user_rating": rating, "anime_status": status, "anime_title": anime["title"]})
        s.commit()
    st.rerun()

def fetch_user_top():
    username = st.session_state.get("username")
    sql_statement = f'''SELECT * FROM {username} WHERE rating > 7;'''
    conn = st.connection("mysql", "sql")
    try:
        with conn.session as s:
            data = s.execute(sql_statement)
    except:
        st.error("Cannot fetch the user table")
    return data

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