# gerer les joueurs
from flask import Blueprint, jsonify, request
from app.models import Player
from app.models import PlayerStat

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

  
@bp.route('/player_stats/<int:player_id>', methods=['GET'])
def get_player_stats(player_id):
    # Recherche du joueur dans la base de données
    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404
    
    # Recherche des statistiques du joueur
    stats = PlayerStat.query.filter_by(player_id=player_id).all()
    if not stats or len(stats) == 0:
        return jsonify({"message": "No statistics available for this player yet. The player has not participated in any games."}), 200

    # Retourner les statistiques sous forme de JSON
    return jsonify([{
        "id": stat.id,
        "games_played": stat.games_played,
        "ppg": str(stat.ppg) if stat.ppg else "0",
        "apg": str(stat.apg) if stat.apg else "0",
        "rpg": str(stat.rpg) if stat.rpg else "0",
        "minutes_played": stat.minutes_played if stat.minutes_played else 0,
        "fgm": str(stat.fgm) if stat.fgm else "0",
        "fga": str(stat.fga) if stat.fga else "0",
        "fg_pct": str(stat.fg_pct) if stat.fg_pct else "0.0",
        "threepm": str(stat.threepm) if stat.threepm else "0",
        "threepa": str(stat.threepa) if stat.threepa else "0",
        "three_pct": str(stat.three_pct) if stat.three_pct else "0.0",
        "ftm": str(stat.ftm) if stat.ftm else "0",
        "fta": str(stat.fta) if stat.fta else "0",
        "ft_pct": str(stat.ft_pct) if stat.ft_pct else "0.0",
        "steals": str(stat.steals) if stat.steals else "0",
        "blocks": str(stat.blocks) if stat.blocks else "0",
        "turnovers": str(stat.turnovers) if stat.turnovers else "0"
    } for stat in stats])
