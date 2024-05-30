import streamlit as st
import requests
from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError
import pandas as pd
from menu import menu_with_redirect

# Helper function to fetch anime data
def search(q, lim):
    query = q.replace(" ", "+")
    url = f"https://myanimelist.net/anime.php?q={query}&cat=anime&show={lim}"
    link = requests.get(url)
    soup = BeautifulSoup(link.text, "lxml")
    div = soup.find("div", class_="js-categories-seasonal js-block-list list").find_next("tr")
    anime_html = div.find_next_siblings("tr")
    animes = []
    id = lim + 1
    for anime in anime_html:
        image = anime.find("a", class_="hoverinfo_trigger").find("img").get("data-src")
        title = anime.find("a", class_="hoverinfo_trigger fw-b fl-l").text.strip()
        rating = anime.find("td", width="50").text.strip()
        animes.append({"id": id, "image":image, "title": title, "rating": rating})
        id += 1
    return animes

# Streamlit app
def main():
    menu_with_redirect()
    st.title("MyAnimeList Search")
    
    # Input for search query
    query = st.text_input("Enter anime search query:")
    
    # Initialize session state for pagination
    if 'page' not in st.session_state:
        st.session_state.page = 0

    if query:
        lim = st.session_state.page * 50
    
        # Display results
        animes = pd.DataFrame(search(query, lim))

        for i, anime in animes.iterrows():
            cols = st.columns(5)
            cols[0].write(anime["id"])
            cols[1].image(anime["image"])
            cols[2].write(anime["title"])
            cols[3].write(anime["rating"])
            with cols[4].expander("Add +"):
                st.markdown("Add Anime: ")
                st.number_input("Rating", min_value=0, max_value=10, key=f"rating_{anime['id']}",
                                     on_change=add_anime, args=(anime,))
                st.selectbox(
                    "Choose Status: ",
                    ("Watching", "Completed", "On-Hold", "Dropped", "Plan to Watch"),
                    key=f"status_{anime['id']}",
                    on_change=add_anime, args=(anime,)
                )
            
        # Pagination controls
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.page > 0:
                if st.button("Previous"):
                    st.session_state.page -= 1
        with col2:
            if len(animes) == 50:  # Only show 'Next' button if there are 50 results
                if st.button("Next"):
                    st.session_state.page += 1

def add_anime(anime):
    rating = st.session_state.get(f"rating_{anime['id']}")
    status = st.session_state.get(f"status_{anime['id']}")
    username = st.session_state.get("username")
    conn = st.connection("mysql", "sql")

    try:
        sql_statement = f'''INSERT INTO {username} (image_link, title, rating, status) VALUES (:anime_image, :anime_title, :user_rating, :anime_status);'''
        with conn.session as s:
            s.execute(sql_statement, {"anime_image": anime["image"], "anime_title": anime["title"], "user_rating": rating, "anime_status": status})
            s.commit()
        st.success("Added Succesfully.")
    except IntegrityError:
        sql_statement = f'''UPDATE {username} SET rating = :user_rating, status = :anime_status WHERE title = :anime_title;'''
        with conn.session as s:
            s.execute(sql_statement, {"user_rating": rating, "anime_status": status, "anime_title": anime["title"]})
            s.commit()
        st.success("Updated Show Successfully")

if __name__ == "__main__":
    main()