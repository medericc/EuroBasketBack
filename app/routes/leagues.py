from flask import Blueprint, jsonify
from app.models import  League
from app import db
# Définition du blueprint pour les routes des ligues
leagues_bp = Blueprint('leagues', __name__)

@leagues_bp.route('/leagues', methods=['GET'])
def get_leagues():
    """
    Récupérer toutes les ligues.
    Retourne :
        - Une liste d'objets JSON représentant les ligues.
    """
    try:
        # Récupérer toutes les ligues depuis la base de données
        leagues = League.query.all()

        # Transformer les objets League en dictionnaires JSON
        leagues_data = [
            {
                "id": league.id,
                "name": league.name,
                "tier": league.tier
            } for league in leagues
        ]

        return jsonify({
            "success": True,
            "data": leagues_data
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
@bp.route('seasons', methods=['GET'])
def get_seasons():
    seasons = Season.query.all()
    return jsonify([{
        "id": season.id,
        "year": season.year,
        "league_id": season.league_id
    } for season in seasons])

@bp.route('seasons', methods=['POST'])
def create_season():
    data = request.json
    try:
        new_season = Season(year=data['year'], league_id=data['league_id'])
        db.session.add(new_season)
        db.session.commit()
        return jsonify({"message": "Season created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
