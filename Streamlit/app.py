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

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", str(text))  # espaces / retours ligne
    return html.escape(text.strip())       # sécurité HTML

def render_card(card):
    title = clean_text(card.get("title", ""))
    desc = clean_text(card.get("description", ""))[:200]
    rarity = card.get("rarity", "common")

    img_url = card.get("image_url", "")

    border = colors.get(rarity, "#444")
    color = colors.get(rarity, "#ffffff")

    st.image(card["image_url"], use_container_width=True)
st.subheader(card["title"])
st.write(card["description"][:200])
st.badge(card.get("rarity", "common"))


if st.button("🎴 Pull card"):
    r = requests.get(f"{API_URL}/pull", timeout=30)
    card = r.json()["result"]

    render_card(card)

    st.write(f"⚔ Power: {card.get('power', 'N/A')}")
