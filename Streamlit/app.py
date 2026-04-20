import streamlit as st
import requests
import os

API_URL = "https://astrogatcha.onrender.com"

st.title("🚀 NASA Gacha")

if st.button("Pull card"):
    r = requests.get(f"{API_URL}/pull", timeout=90) 
    card = r.json()["result"]

    st.image(card["image_url"])
    st.write(card["title"])
    st.write(card["rarity"])
    st.write(card["power"])
