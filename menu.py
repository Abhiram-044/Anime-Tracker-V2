import streamlit as st

def authenticated_menu():
    st.sidebar.page_link("pages/user_shows.py", label="Your profile")
    st.sidebar.page_link("pages/top.py", label="Top")
    st.sidebar.page_link("pages/search.py", label="Search")
    st.sidebar.page_link("pages/recommendation_page.py", label="Recommended")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}) and st.rerun(), key="Logout")

def unauthenticated_menu():
    st.sidebar.page_link("app.py", label="Log in")

def menu():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        unauthenticated_menu()
    else:
        authenticated_menu()

def menu_with_redirect():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.session_state.current_page = "app.py"
    menu()