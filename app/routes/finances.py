from flask import Blueprint, request, jsonify
from app.models import Finance, Team
from app import db
bp = Blueprint('finances', __name__, url_prefix='/finances')

@bp.route('/team/<int:team_id>', methods=['GET'])
def get_team_finances(team_id):
    """
    Obtenir les finances d'une équipe, y compris les revenus et les dépenses.
    """
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
                "type": finance.type,  # 'revenue' or 'expense'
                "amount": str(finance.amount),
                "description": finance.description,
                "date": finance.date
            } for finance in finances]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/team/<int:team_id>', methods=['POST'])
def add_team_finance(team_id):
    """
    Ajouter une transaction financière pour une équipe (revenus ou dépenses).
    """
    data = request.json
    try:
        team = Team.query.get(team_id)
        if not team:
            return jsonify({"error": "Team not found"}), 404

        finance = Finance(
            team_id=team_id,
            type=data['type'],  # 'revenue' or 'expense'
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
