import streamlit as st

def main():
    st.title("Welcome to Anime-Tracker")

    conn = st.connection("mysql", "sql")

    conn