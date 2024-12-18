# gerer les matchs
from flask import Blueprint, request, jsonify
from app.models import Game, db

bp = Blueprint('games', __name__, url_prefix='/games')

@bp.route('/', methods=['GET'])
def get_games():
    games = Game.query.all()
    return jsonify([{
        "id": game.id,
        "season_id": game.season_id,
        "home_team_id": game.home_team_id,
        "away_team_id": game.away_team_id,
        "date": game.date,
        "home_score": game.home_score,
        "away_score": game.away_score
    } for game in games])

@bp.route('/', methods=['POST'])
def create_game():
    data = request.json
    try:
        new_game = Game(
            season_id=data['season_id'],
            home_team_id=data['home_team_id'],
            away_team_id=data['away_team_id'],
            date=data['date'],
            home_score=data.get('home_score', 0),
            away_score=data.get('away_score', 0)
        )
        db.session.add(new_game)
        db.session.commit()
        return jsonify({"message": "Game created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
