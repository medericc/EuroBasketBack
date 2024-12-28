from flask import Blueprint, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
import os

bp = Blueprint('career', __name__)

@bp.route('/create_career', methods=['POST'])
def create_career():
    """
    Crée ou réinitialise une base de données dynamique `career_basket`.
    """
    admin_db_url = os.getenv('ADMIN_DB_URL')
    db_url_prefix = os.getenv('DB_URL_PREFIX')
    base_db_name = "basket"
    career_db_name = "career_basket"
    career_db_url = f"{db_url_prefix}{career_db_name}"

    if not admin_db_url or not db_url_prefix:
        return jsonify({"error": "ADMIN_DB_URL ou DB_URL_PREFIX non configuré"}), 500

    try:
        # Connexion avec les privilèges admin
        admin_engine = create_engine(admin_db_url)
        
        # Activer AUTOCOMMIT explicitement
        with admin_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            # Terminer les connexions actives à la base source (basket)
            conn.execute(text(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='{base_db_name}';"))
            print(f"Connexions actives sur la base {base_db_name} terminées.")

            # Terminer les connexions actives à la base cible (career_basket)
            conn.execute(text(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='{career_db_name}';"))
            print(f"Connexions actives sur la base {career_db_name} terminées.")
            
            # Supprimer la base cible si elle existe
            conn.execute(text(f"DROP DATABASE IF EXISTS {career_db_name};"))
            print(f"Base de données {career_db_name} supprimée avec succès.")
            
            # Créer une nouvelle base en copiant le modèle existant
            conn.execute(text(f"CREATE DATABASE {career_db_name} TEMPLATE {base_db_name};"))
            print(f"Base de données {career_db_name} créée avec succès à partir du modèle '{base_db_name}'.")
        
        return jsonify({"message": f"Base de données `{career_db_name}` créée avec succès."}), 200
    
    except ProgrammingError as e:
        print(f"Erreur SQL : {str(e)}")
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        print(f"Erreur inattendue : {str(e)}")
        return jsonify({"error": f"Erreur inattendue : {str(e)}"}), 500
