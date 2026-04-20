- Installer docker
- DL les fichiers depuis Git et les insérer dans le même dossier
- Lancer Docker
- Depuis Airflow, trouver le DAG nasa_image_pipeline et le lancer

  --> Extract = récupère 100 lignes depuis l'API "https://images-api.nasa.gov/search?q=galaxy&media_type=image"
  --> Transform = conserve les colonnes href, title, description, date_created, keywords
  --> Récupère les images associées aux href
  --> Load = charge vers MongoDB (base dans Docker)
