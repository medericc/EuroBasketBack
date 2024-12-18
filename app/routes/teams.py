# team gerer
from flask import Blueprint, request, jsonify
from app.models import Team, db

bp = Blueprint('teams', __name__, url_prefix='/teams')

@bp.route('/', methods=['GET'])
def get_teams():
    teams = Team.query.all()
    return jsonify([{
        "id": team.id,
        "name": team.name,
        "league_id": team.league_id,
        "budget": str(team.budget)
    } for team in teams])

@bp.route('/', methods=['POST'])
def create_team():
    data = request.json
    try:
        new_team = Team(
            name=data['name'],
            league_id=data['league_id'],
            budget=data.get('budget', 0)
        )
        db.session.add(new_team)
        db.session.commit()
        return jsonify({"message": "Team created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
