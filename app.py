import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("🚀 NASA Gacha Game")

# -------------------------
# PULL CARD
# -------------------------
if st.button("🎲 Pull 1 card"):
    response = requests.get(f"{API_URL}/pull")
    card = response.json()["result"]

    st.image(card["image_url"])
    st.subheader(card["title"])
    st.write("⭐ Rarity:", card["rarity"])
    st.write("⚔️ Power:", card["power"])

# -------------------------
# COLLECTION
# -------------------------
st.divider()
st.subheader("📚 Collection")

cards = requests.get(f"{API_URL}/cards").json()

for c in cards[:20]:
    st.write(f"{c['title']} - {c['rarity']}")
