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



def render_card(card):
    st.markdown(
        f"""
        <div style="
            border-radius: 16px;
            padding: 12px;
            background: linear-gradient(145deg, #1e1e2f, #2a2a40);
            box-shadow: 0px 4px 12px rgba(0,0,0,0.35);
            margin-bottom: 12px;
            color: white;
            height: 420px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        ">
            <h4 style="text-align:center; margin:5px 0;">
                {card.get('title','')}
            </h4>

            <img src="{card.get('image_url','')}"
                 style="width:100%; height:180px; object-fit:cover; border-radius:10px;">

            <p style="
                font-size:12px;
                opacity:0.8;
                overflow:hidden;
                display:-webkit-box;
                -webkit-line-clamp:4;
                -webkit-box-orient:vertical;
            ">
                {card.get('description','')[:200]}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )



if st.button("🎴 Pull card"):
    r = requests.get(f"{API_URL}/pull", timeout=30)
    card = r.json()["result"]  
    
    color = colors.get(card["rarity"], "#ffffff")
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
    st.header(card["power"], text_alignment="right")
    st.image(card["image_url"])
    st.write(card["title"])
    st.write(card["description"])
    
    
