from sqlalchemy import create_engine

def get_user_db_engine(user_db_url):
    """Retourne un moteur SQLAlchemy connecté à la base de données utilisateur."""
    return create_engine(user_db_url)