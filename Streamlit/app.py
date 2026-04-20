import streamlit as st
import requests
import os

API_URL = "https://astrogatcha.onrender.com"

st.title("Clique putain je t'emmène voir les étoiles...")

def render_card(card):
    st.markdown(
        f"""
        <div style="
            border-radius: 15px;
            padding: 15px;
            background: linear-gradient(145deg, #1e1e2f, #2a2a40);
            box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
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

if st.button("🎴 Pull card"):
    r = requests.get(f"{API_URL}/pull", timeout=30)
    card = r.json()["result"]
    st.write(r.text)
    st.image(card["image_url"])
    st.write(card["title"])
    st.image(card["description"])
    st.write(card["rarity"])
    st.write(card["power"])
