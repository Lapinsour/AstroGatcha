from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

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
    response = requests.get(NASA_URL)
    data = response.json()
    context["ti"].xcom_push(key="raw_data", value=data)


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


def load_to_mongo(**context):
    ti = context["ti"]

    df_json = ti.xcom_pull(task_ids="download_images", key="df_final")

    if df_json is None:
        raise ValueError("XCom df_final est vide (download_images n'a rien poussé ou pull incorrect)")

    df = pd.read_json(df_json)

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

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

    t_mongo = PythonOperator(
        task_id="load_mongo",
        python_callable=load_to_mongo
    )

    t_extract >> t_transform >> t_images >> t_mongo