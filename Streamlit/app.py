import streamlit as st
import requests
import re
import html

API_URL = "https://astrogatcha.onrender.com"

st.title("🌌 Clique pour explorer les étoiles")

colors = {
    "common": "#9aa0a6",
    "rare": "#4F8BF9",
    "epic": "#A855F7",
    "legendary": "#FBBF24"
}

def render_card(card):  
    rarity = card.get("rarity", "common")        
    border = colors.get(rarity, "#444")
    color = colors.get(rarity, "#ffffff")

    # badge rarity
    st.markdown(
        f"""
        <div style="
            display:inline-block;
            padding:4px 10px;
            border-radius:8px;
            background-color:{color};
            color:black;
            font-weight:bold;
            font-size:12px;
        ">
            {rarity}
        </div>
        """,
        unsafe_allow_html=True
    )
    


if st.button("🎴 Pull card"):
    r = requests.get(f"{API_URL}/pull", timeout=30)
    card = r.json()["result"]

    render_card(card)

    
