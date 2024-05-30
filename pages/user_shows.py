import streamlit as st
from menu import menu_with_redirect
import pandas as pd

def main():
    menu_with_redirect()
    st.title("User Shows")
    data = get_user_list()
    rows = pd.DataFrame(data)
    for i, anime in rows.iterrows():
        cols = st.columns(6)
        cols[0].write(i + 1)
        cols[1].image(anime["image_link"])
        cols[2].write(anime["title"])
        cols[3].write(anime["rating"])
        cols[4].write(anime["status"])
        with cols[5].expander("Update"):
            st.markdown("Update Anime")
            st.number_input("Rating", min_value=0, max_value=10, key=f"rating_{i+1}",
                            on_change=update_anime, args = (anime, i))
            st.selectbox(
                "Choose Status: ",
                ("Watching", "Completed", "On-Hold", "Dropped", "Plan to Watch"),
                key=f"status_{i+1}",
                on_change=update_anime, args=(anime, i)
            )
            if st.button("change", key=f"button_{i}"):
                st.rerun()




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


def get_user_list():
    conn = st.connection("mysql", "sql")
    username = st.session_state.get("username")
    try:
        sql_statment = f'''SELECT * FROM {username};'''
        with conn.session as s:
            data = s.execute(sql_statment)
    except:
        st.error("Cannot fetch the user table")
    return data

if __name__ == "__main__":
    main()