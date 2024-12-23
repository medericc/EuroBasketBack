from flask import Blueprint, request, jsonify
from app import get_dynamic_model, db
from utils.season_validators import validate_season_data

bp = Blueprint('seasons', __name__, url_prefix='/seasons')

def get_models(username, user_db_url):
    """Récupère les modèles dynamiques nécessaires"""
    models = get_dynamic_model(username, user_db_url)
    return models.get('seasons'), models.get('leagues')

@bp.route('/', methods=['GET'])
def get_seasons():
    """Récupérer toutes les saisons."""
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    
    if not username or not user_db_url:
        return jsonify({'error': 'username et user_db_url sont requis'}), 400
        
    Season, _ = get_models(username, user_db_url)
    if not Season:
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404
        
    seasons = Season.query.all()
    return jsonify([{
        "id": season.id,
        "start_year": season.start_year,
        "end_year": season.end_year
    } for season in seasons])

@bp.route('/', methods=['POST'])
def create_season():
    """Créer une nouvelle saison."""
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    data = request.json
    
    if not username or not user_db_url:
        return jsonify({'error': 'username et user_db_url sont requis'}), 400
        
    Season, League = get_models(username, user_db_url)
    if not all([Season, League]):
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404
        
    # Valider les données
    is_valid, error_message = validate_season_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400
        
    try:
        new_season = Season(
            start_year=data['start_year'],
            end_year=data['end_year']
        )
        db.session.add(new_season)
        db.session.commit()
        return jsonify({"message": "Season created"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400