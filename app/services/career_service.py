from utils.db_utils import get_user_db_engine
from sqlalchemy import text
from sql.career_tables import get_drop_tables_sql, get_create_tables_sql

def create_career_tables(user_db_url, username):
    """Crée les tables spécifiques à une carrière avec un préfixe unique."""
    try:
        engine = get_user_db_engine(user_db_url)
        with engine.connect() as conn:
            conn.execute(text(get_drop_tables_sql(username)))
            conn.execute(text(get_create_tables_sql(username)))
            conn.commit()
        return True, "Tables de carrière créées avec succès."
    except Exception as e:
        return False, f"Erreur lors de la création des tables : {str(e)}"