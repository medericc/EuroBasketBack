from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData, Table
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
# Charge les variables d'environnement depuis le fichier .env
load_dotenv()

# Extensions Flask
db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """
    Initialise la base de données pour l'application Flask.
    Configure SQLAlchemy et applique les migrations.
    """
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise RuntimeError("DATABASE_URL n'est pas défini dans le fichier .env.")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()


    """
    Crée une base de données PostgreSQL spécifique pour un utilisateur.
    :param user_identifier: Identifiant unique de l'utilisateur.
    """
    # Récupère la partie fixe de l'URL de base de données
    db_url_prefix = os.getenv('DB_URL_PREFIX')
    if not db_url_prefix:
        raise RuntimeError("La partie fixe de l'URL de la base de données n'est pas définie dans le fichier .env.")

    # Génère le nom de la base de données utilisateur
    user_db_name = f"career_{user_identifier}_"
    user_db_url = db_url_prefix + user_db_name

    # Utilise une URL d'administration pour se connecter au serveur PostgreSQL
    admin_db_url = os.getenv('ADMIN_DB_URL')  # URL pour administrer PostgreSQL
    if not admin_db_url:
        raise RuntimeError("L'URL d'administration PostgreSQL (ADMIN_DB_URL) n'est pas définie dans le fichier .env.")

    # Connexion au serveur PostgreSQL
    engine = create_engine(admin_db_url)
    connection = engine.connect()

    try:
        # Création de la base de données utilisateur
        connection.execute(f"CREATE DATABASE {user_db_name}")
        print(f"Base de données {user_db_name} créée avec succès.")
    except ProgrammingError as e:
        if "already exists" in str(e):
            print(f"La base de données {user_db_name} existe déjà.")
        else:
            raise
    finally:
        connection.close()