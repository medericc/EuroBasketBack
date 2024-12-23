from flask import Blueprint, request, jsonify
from app import get_dynamic_model, db

bp = Blueprint('finances', __name__, url_prefix='/finances')

def get_models(username, user_db_url):
    """Récupère les modèles dynamiques nécessaires"""
    models = get_dynamic_model(username, user_db_url)
    return models.get('finances'), models.get('teams')

@bp.route('/team/<int:team_id>', methods=['GET'])
def get_team_finances(team_id):
    """
    Obtenir les finances d'une équipe, y compris les revenus et les dépenses.
    """
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    
    if not username or not user_db_url:
        return jsonify({'error': 'username et user_db_url sont requis'}), 400
        
    Finance, Team = get_models(username, user_db_url)
    if not all([Finance, Team]):
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404
    
    try:
        team = Team.query.get(team_id)
        if not team:
            return jsonify({"error": "Team not found"}), 404

        finances = Finance.query.filter_by(team_id=team_id).all()
        return jsonify({
            "team": {
                "id": team.id,
                "name": team.name
            },
            "finances": [{
                "id": finance.id,
                "type": finance.type,
                "amount": str(finance.amount),
                "description": finance.description,
                "date": finance.date.isoformat() if finance.date else None
            } for finance in finances]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/team/<int:team_id>', methods=['POST'])
def add_team_finance(team_id):
    """
    Ajouter une transaction financière pour une équipe (revenus ou dépenses).
    """
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    data = request.json
    
    if not username or not user_db_url:
        return jsonify({'error': 'username et user_db_url sont requis'}), 400
        
    Finance, Team = get_models(username, user_db_url)
    if not all([Finance, Team]):
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404
    
    try:
        team = Team.query.get(team_id)
        if not team:
            return jsonify({"error": "Team not found"}), 404

        finance = Finance(
            team_id=team_id,
            type=data['type'],
            amount=data['amount'],
            description=data.get('description', ''),
            date=data['date']
        )

        db.session.add(finance)
        db.session.commit()
        return jsonify({"message": "Finance transaction added successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400