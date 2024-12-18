# gerer les joueurs
from flask import Blueprint, jsonify, request
from app.models import Player, db

bp = Blueprint('players', __name__, url_prefix='/players')

@bp.route('/', methods=['GET'])
def get_players():
    players = Player.query.all()
    return jsonify([{
        "id": player.id,
        "first_name": player.first_name,
        "last_name": player.last_name,
        "position": player.position,
        "market_value": str(player.market_value)
    } for player in players])

@bp.route('/', methods=['POST'])
def create_player():
    data = request.json
    new_player = Player(
        first_name=data['first_name'],
        last_name=data['last_name'],
        position=data['position'],
        height=data['height'],
        weight=data['weight'],
        birth_date=data['birth_date'],
        market_value=data['market_value']
    )
    db.session.add(new_player)
    db.session.commit()
    return jsonify({"message": "Player created"}), 201
