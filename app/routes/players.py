# gerer les joueurs
from flask import Blueprint, jsonify, request
from app.models import Player
from app import db
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
@bp.route('/<int:id>', methods=['GET'])
def get_player_details(id):
    player = Player.query.get(id)
    if not player:
        return jsonify({"error": "Player not found"}), 404
    return jsonify({
        "id": player.id,
        "first_name": player.first_name,
        "last_name": player.last_name,
        "position": player.position,
        "height": str(player.height),
        "weight": str(player.weight),
        "birth_date": player.birth_date.strftime('%Y-%m-%d'),
        "market_value": str(player.market_value),
        "team_id": player.team_id
    })
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
@bp.route('/<int:id>', methods=['PUT'])
def update_player(id):
    data = request.json
    player = Player.query.get(id)
    if not player:
        return jsonify({"error": "Player not found"}), 404
    try:
        player.first_name = data.get('first_name', player.first_name)
        player.last_name = data.get('last_name', player.last_name)
        player.position = data.get('position', player.position)
        player.height = data.get('height', player.height)
        player.weight = data.get('weight', player.weight)
        player.market_value = data.get('market_value', player.market_value)
        db.session.commit()
        return jsonify({"message": "Player updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/<int:id>', methods=['DELETE'])
def delete_player(id):
    player = Player.query.get(id)
    if not player:
        return jsonify({"error": "Player not found"}), 404
    try:
        db.session.delete(player)
        db.session.commit()
        return jsonify({"message": "Player deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/team/<int:team_id>', methods=['GET'])
def get_players_by_team(team_id):
    players = Player.query.filter_by(team_id=team_id).all()
    return jsonify([
        {
            "id": player.id,
            "first_name": player.first_name,
            "last_name": player.last_name,
            "position": player.position,
            "market_value": str(player.market_value)
        } for player in players
    ])