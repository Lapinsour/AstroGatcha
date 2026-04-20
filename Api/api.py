from fastapi import FastAPI
from pymongo import MongoClient
import random

app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["nasa"]

# -------------------------
# GET ALL CARDS
# -------------------------
@app.get("/cards")
def get_cards():
    return list(db.cards.find({}, {"_id": 0}))


# -------------------------
# GACHA PULL
# -------------------------
@app.get("/pull")
def pull_card():
    cards = list(db.cards.find({}, {"_id": 0}))

    if not cards:
        return {"error": "No cards found"}

    card = random.choice(cards)
    return {
        "result": card
    }
