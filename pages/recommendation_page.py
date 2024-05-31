from recommendation import find_similar_animes
import streamlit as st
from sqlalchemy.exc import IntegrityError
from menu import menu_with_redirect
import pandas as pd
from sql_commands import add_anime, fetch_user_top

if "rec_no" not in st.session_state:
        st.session_state["rec_no"] = 0

def main():
    menu_with_redirect()
    
    st.title("Recommendation based on Your Preferences: ")
    top_animes = pd.DataFrame(fetch_user_top())
    top_anime = top_animes.iloc[st.session_state.get("rec_no")]
    anime_name = top_anime['title']
    anime_image = top_anime['image_link']
    recs = pd.DataFrame(find_similar_animes(anime_name))

    st.write("Because you liked this")
    cols1 = st.columns(2)
    cols1[0].image(anime_image, width=50)
    cols1[1].title(anime_name)


    for i, rec in recs.iterrows():
        cols = st.columns(6)
        cols[0].write(rec["id"])
        cols[1].image(rec["image"], width=50)
        cols[2].write(rec["title"])
        cols[3].write(rec["similarity"])
        cols[4].write(rec["rating"])
        with cols[5].expander("Add +"):
            st.markdown("Add Anime: ")
            st.number_input("Rating", min_value=0, max_value=10, key=f"rating_{rec['id']}",
                                     on_change=add_anime, args=(rec,))
            st.selectbox(
                "Choose Status: ",
                ("Watching", "Completed", "On-Hold", "Dropped", "Plan to Watch"),
                key=f"status_{rec['id']}",
                on_change=add_anime, args=(rec,)
            )
    
    col1, col2 = st.columns(2)
    with col1:
         if st.session_state.rec_no > 0:
              if st.button("Previous"):
                   st.session_state.rec_no -= 1
    with col2:
        if st.button("Next"):
            st.session_state.rec_no += 1
              


if __name__ == "__main__":
     main()