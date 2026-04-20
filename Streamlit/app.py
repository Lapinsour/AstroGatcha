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
    
    st.badge(card.get("rarity", "common"))
    st.header(card["power"], text_alignment="right")
    
    st.image(card["image_url"], 100)
    st.subheader(card["title"], text_alignment="center")
    st.write(card["description"][:200])
    


if st.button("🎴 Pull card"):
    r = requests.get(f"{API_URL}/pull", timeout=30)
    card = r.json()["result"]

    render_card(card)

    
