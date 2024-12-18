from dotenv import load_dotenv
import os

# Charger les variables depuis le fichier .env
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("DATABASE_URL n'est pas défini dans le fichier .env")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = os.getenv("CORS_HEADERS", "Content-Type")
