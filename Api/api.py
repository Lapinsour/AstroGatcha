import os
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
    count = db.cards.count_documents({})

    if count == 0:
        return {"error": "No cards found"}

    random_index = random.randint(0, count - 1)
    card = db.cards.find().skip(random_index).limit(1)[0]

    return {"result": card}
