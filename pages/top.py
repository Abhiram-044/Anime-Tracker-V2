import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from sqlalchemy.exc import IntegrityError
from menu import menu_with_redirect
from sql_commands import add_anime

if 'lim1' not in st.session_state:
    st.session_state.lim1 = 0

def main():
    menu_with_redirect()
    st.title("Top Rated Shows")
    animes = pd.DataFrame(top(st.session_state.lim1))
    
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
        
    cols2 = st.columns(2)
    if cols2[0].button("Prev 50"):
        if st.session_state.lim1 > 0:
            st.session_state.lim1 -= 50
            st.rerun()
        else:
            st.error("No Previous pages available")
        
    if cols2[1].button("Next 50"):
        st.session_state.lim1 += 50
        st.rerun()

def top(lim):
    url = f"https://myanimelist.net/topanime.php?limit={lim}"
    link = requests.get(url)
    soup = BeautifulSoup(link.text, "lxml")
    anime_html = soup.find_all("tr", class_="ranking-list")
    animes = []
    id = lim + 1

    for anime in anime_html:
        image = anime.find("a", class_="hoverinfo_trigger fl-l ml12 mr8").find("img").get("data-src")
        title = anime.find("h3", class_="fl-l fs14 fw-b anime_ranking_h3").find("a").text.strip()
        rating = anime.find("span", class_=re.compile(r"^text on score-label score-\d+$")).text.strip()
        animes.append(
            {
            "id": id,
            "image": image,
            "title": title,
            "rating": rating
            }
        )
        id += 1

    return animes


if __name__ == "__main__":
    main()