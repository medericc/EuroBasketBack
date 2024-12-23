from flask import Blueprint, request, jsonify
from app import get_dynamic_model, db

bp = Blueprint('leagues', __name__, url_prefix='/leagues')

def get_models(username, user_db_url):
    """Récupère les modèles dynamiques nécessaires"""
    models = get_dynamic_model(username, user_db_url)
    return models.get('leagues'), models.get('seasons')

@bp.route('/', methods=['GET'])
def get_leagues():
    """Récupérer toutes les ligues."""
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    
    if not username or not user_db_url:
        return jsonify({'error': 'username et user_db_url sont requis'}), 400
        
    League, _ = get_models(username, user_db_url)
    if not League:
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404
        
    try:
        leagues = League.query.all()
        return jsonify({
            "success": True,
            "data": [{
                "id": league.id,
                "name": league.name,
                "tier": league.tier
            } for league in leagues]
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500