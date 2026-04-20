import streamlit as st
import requests
import re
import html

API_URL = "https://astrogatcha.onrender.com"



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
    shadow_strength = "0 0 20px" if rarity in ["epic", "legendary"] else "0 0 10px"

    st.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin:8px 0;
        ">
            <div style="
                font-size:16px;
                font-weight:bold;
                color:white;
            ">
                ⚔ {card.get("power", "N/A")}
            </div>
    
            <div style="
                padding:4px 10px;
                border-radius:8px;
                background-color:{color};
                color:black;
                font-weight:bold;
                font-size:12px;
            ">
                {rarity}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    ) 

    st.markdown(
        f"""
        <div style="
            border: 3px solid {color};
            border-radius: 12px;
            padding: 3px;
            box-shadow: {shadow_strength} {color};
            height: 380px;
            overflow: hidden;         
        ">
            <img src="{card.get('image_url','')}"
                 style="
                    width:100%;
                    height:auto;
                    object-fit: cover;
                    border-radius: 10px;
                    display:block;
                 ">
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.subheader(card["title"], text_alignment="center")
    st.write(card["description"][:200])

if st.button("🎴 Pull card"):
    r = requests.get(f"{API_URL}/pull", timeout=30)
    card = r.json()["result"]

    render_card(card)

    
