from flask import Blueprint, request, jsonify
from app import db
bp = Blueprint('players', __name__, url_prefix='/players')

def get_models(username, user_db_url):
    """Récupère les modèles dynamiques nécessaires"""
    models = (username, user_db_url)
    return models.get('players'), models.get('player_stats')

@bp.route('/', methods=['GET'])
def get_players():
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    
    if not username or not user_db_url:
        return jsonify({'error': 'username et user_db_url sont requis'}), 400
        
    Player, _ = get_models(username, user_db_url)
    if not Player:
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404
        
    players = Player.query.all()
    return jsonify([{
        "id": player.id,
        "first_name": player.first_name,
        "last_name": player.last_name,
        "position": player.position,
        "market_value": str(player.market_value)
    } for player in players])

@bp.route('/<int:player_id>/stats', methods=['GET'])
def get_player_stats(player_id):
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    
    if not username or not user_db_url:
        return jsonify({'error': 'username et user_db_url sont requis'}), 400
        
    Player, PlayerStat = get_models(username, user_db_url)
    if not all([Player, PlayerStat]):
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404
        
    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Player not found"}), 404
        
    stats = PlayerStat.query.filter_by(player_id=player_id).all()
    return jsonify([{
        "id": stat.id,
        "games_played": stat.games_played,
        "ppg": str(stat.ppg),
        "apg": str(stat.apg),
        "rpg": str(stat.rpg),
        "minutes_played": stat.minutes_played,
        "fgm": str(stat.fgm),
        "fga": str(stat.fga),
        "fg_pct": str(stat.fg_pct),
        "threepm": str(stat.threepm),
        "threepa": str(stat.threepa),
        "three_pct": str(stat.three_pct),
        "ftm": str(stat.ftm),
        "fta": str(stat.fta),
        "ft_pct": str(stat.ft_pct),
        "steals": str(stat.steals),
        "blocks": str(stat.blocks),
        "turnovers": str(stat.turnovers)
    } for stat in stats])