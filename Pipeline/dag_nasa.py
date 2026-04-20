from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import random
import requests
import pandas as pd
from pymongo import MongoClient
from PIL import Image
from io import BytesIO


NASA_URL = "https://images-api.nasa.gov/search?q=galaxy&media_type=image"
MONGO_URI = "mongodb://mongo:27017/"
DB_NAME = "nasa"
COLLECTION_NAME = "images"
IMAGE_SIZE = (256, 256)


# =========================
# TASKS
# =========================

def extract(**context):
    base_url = "https://images-api.nasa.gov/search"
    params = {
        "q": "galaxy",
        "media_type": "image"
    }

    all_items = []
    url = base_url

    for _ in range(10):  # ~100 pages max selon API (sécurité)
        response = requests.get(url, params=params if url == base_url else None)
        data = response.json()

        items = data["collection"]["items"]
        all_items.extend(items)

        # pagination
        links = data["collection"].get("links", [])
        next_link = None

        for l in links:
            if l.get("rel") == "next":
                next_link = l.get("href")

        if not next_link:
            break

        url = next_link
        params = None  # déjà inclus dans next_link

        # stop à 1000 éléments
        if len(all_items) >= 1000:
            all_items = all_items[:1000]
            break

    context["ti"].xcom_push(key="raw_data", value={"collection": {"items": all_items}})


def transform(**context):
    ti = context["ti"]

    data = ti.xcom_pull(task_ids="extract", key="raw_data")

    if data is None:
        raise ValueError("XCom raw_data est vide (extract n'a rien poussé ou pull incorrect)")

    items = data["collection"]["items"]

    df_data = pd.json_normalize([i["data"][0] for i in items])
    df_links = [i.get("links", [{}])[0].get("href") for i in items]

    df = df_data.copy()
    df["href"] = df_links

    df = df[['href', 'title', 'description', 'date_created', 'keywords']]

    ti.xcom_push(key="df", value=df.to_json())





def download_images(**context):
    ti = context["ti"]

    df_json = ti.xcom_pull(task_ids="transform", key="df")

    if df_json is None:
        raise ValueError("XCom df est vide (transform n'a rien poussé ou pull incorrect)")

    df = pd.read_json(df_json)

    images = []

    for url in df["href"]:
        try:
            r = requests.get(url, timeout=10)
            img = Image.open(BytesIO(r.content)).convert("RGB")
            img = img.resize(IMAGE_SIZE)
            images.append(True)
        except:
            images.append(False)

    df["image_ok"] = images
    df = df[df["image_ok"] == True]

    ti.xcom_push(key="df_final", value=df.to_json())


def assign_rarity():
    r = random.random()
    if r < 0.6:
        return "common"
    elif r < 0.85:
        return "rare"
    elif r < 0.97:
        return "epic"
    else:
        return "legendary"


RARITY_POWER = {
    "common": 10,
    "rare": 25,
    "epic": 50,
    "legendary": 100
}


def build_cards_dataset(**context):
    ti = context["ti"]

    df_json = ti.xcom_pull(task_ids="download_images", key="df_final")

    if df_json is None:
        raise ValueError("XCom df_final est vide")

    df = pd.read_json(df_json)

    # -------------------------
    # CARD TRANSFORMATION
    # -------------------------

    df = df.dropna(subset=["href", "title"])

    df["id"] = df.index.astype(str)
    df["image_url"] = df["href"]

    df["rarity"] = df["title"].apply(lambda x: assign_rarity())
    df["power"] = df["rarity"].map(RARITY_POWER)

    df["card_type"] = "nasa_image"

    cards_df = df[[
        "id",
        "title",
        "description",
        "image_url",
        "rarity",
        "power",
        "card_type"
    ]]

    ti.xcom_push(key="cards_df", value=cards_df.to_json())


def load_to_mongo(**context):
    ti = context["ti"]

    df_json = ti.xcom_pull(task_ids="build_cards", key="cards_df")

    if df_json is None:
        raise ValueError("XCom cards_df est vide")

    df = pd.read_json(df_json)

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["cards"]   # 👈 nouvelle collection

    records = df.to_dict(orient="records")

    collection.insert_many(records)


# =========================
# DAG
# =========================

default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 1
}

with DAG(
    dag_id="nasa_image_pipeline",
    schedule="@daily",
    default_args=default_args,
    catchup=False
) as dag:

    t_extract = PythonOperator(
        task_id="extract",
        python_callable=extract
    )

    t_transform = PythonOperator(
        task_id="transform",
        python_callable=transform
    )

    t_images = PythonOperator(
        task_id="download_images",
        python_callable=download_images
    )

    t_cards = PythonOperator(
        task_id="build_cards",
        python_callable=build_cards_dataset
    )

    t_mongo = PythonOperator(
        task_id="load_mongo",
        python_callable=load_to_mongo
    )

    t_extract >> t_transform >> t_images >> t_cards >> t_mongo
