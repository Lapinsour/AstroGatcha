import streamlit as st
import requests
import os

API_URL = "https://astrogatcha.onrender.com"

st.title("Clique putain je t'emmène voir les étoiles...")

colors = {
    "common": "#9aa0a6",
    "rare": "#4F8BF9",
    "epic": "#A855F7",
    "legendary": "#FBBF24"
}

color = colors.get(card["rarity"], "#ffffff")

def render_card(card):
    st.markdown(
        f"""
        <div style="
            border-radius: 150px;
            padding: 150px;
            background: linear-gradient(145deg, #1e1e2f, #2a2a40);
            box-shadow: 0px 4px 50px rgba(0,0,0,0.4);
            margin-bottom: 20px;
            color: white;
        ">
            <h3 style="text-align:center;">{card.get('title','')}</h3>
            <img src="{card.get('image_url','')}" style="width:100%; border-radius:10px;">
            <p style="font-size:14px; opacity:0.8;">{card.get('description','')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

cols = st.columns(3)



if st.button("🎴 Pull card"):
    r = requests.get(f"{API_URL}/pull", timeout=30)
    card = r.json()["result"]
    
    st.image(card["image_url"])
    st.write(card["title"])
    st.write(card["description"])
    st.markdown(
    f"""
    <div style="
        text-align:right;
        background-color:{color};
        color:black;
        padding:5px 10px;
        border-radius:8px;
        display:inline-block;
    ">
        {card['rarity']}
    </div>
    """,
    unsafe_allow_html=True
)
   
    st.write(card["power"])
