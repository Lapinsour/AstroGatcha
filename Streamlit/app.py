import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://api:8000")

st.title("🚀 NASA Gacha")

if st.button("Pull card"):
    r = requests.get(f"{API_URL}/pull")
    card = r.json()["result"]

    st.image(card["image_url"])
    st.write(card["title"])
    st.write(card["rarity"])
    st.write(card["power"])
