import streamlit as st

def authenticated_menu():
    st.sidebar.page_link("main", label="Switch Accounts")
    st.sidebar.page_link("pages/user_shows", label="Your profile")
    st.sidebar.page_link("pages/top", label="Top")
    st.sidebar.page_link("pages/search", label="Search")

def unauthenticated_menu():
    st.sidebar.page_link("main", label="Log in")

def menu():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        unauthenticated_menu()
    else:
        authenticated_menu()

def menu_with_redirect():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.session_state.current_page = "main"
    menu()