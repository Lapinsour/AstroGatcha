import json
import random
from fastapi import FastAPI
import os

app = FastAPI()

CARDS = []
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "cards_nasa.json")
with open(FILE_PATH, "r", encoding="utf-8") as f:
    for line in f:
        CARDS.append(json.loads(line))

@app.get("/pull")
def pull_card():
    if not CARDS:
        return {"error": "No cards"}

    return {"result": random.choice(CARDS)}


'''
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
# GACHA PULL (FIXED)
# -------------------------
@app.get("/pull")
def pull_card():
    card = db.cards.aggregate([
        {"$sample": {"size": 1}}
    ])

    result = next(card, None)

    if result is None:
        return {"error": "No cards found"}

    result.pop("_id", None)

    return {"result": result}
    '''
