# team gerer
from flask import Blueprint, request, jsonify
from app.models import Team
from app import db
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
@bp.route('/<int:id>', methods=['GET'])
def get_team_details(id):
    team = Team.query.get(id)
    if not team:
        return jsonify({"error": "Team not found"}), 404
    return jsonify({
        "id": team.id,
        "name": team.name,
        "league_id": team.league_id,
        "budget": str(team.budget),
        "players": [
            {
                "id": player.id,
                "first_name": player.first_name,
                "last_name": player.last_name,
                "position": player.position
            } for player in team.players
        ]
    })
@bp.route('/league/<int:league_id>', methods=['GET'])
def get_teams_by_league(league_id):
    teams = Team.query.filter_by(league_id=league_id).all()
    if not teams:
        return jsonify({"error": "No teams found for this league"}), 404
    return jsonify([{
        "id": team.id,
        "name": team.name,
        "budget": str(team.budget),
        "logo": team.logo  # Inclure le logo
    } for team in teams])
@bp.route('/team/<int:team_id>', methods=['GET'])
def get_players_by_team(team_id):
    players = Player.query.filter_by(team_id=team_id).all()
    if not players:
        return jsonify({"error": "No players found for this team"}), 404
    
    # Récupérer les statistiques de chaque joueur
    players_with_stats = []
    for player in players:
        stats = PlayerStat.query.filter_by(player_id=player.id).all()
        player_stats = [{
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
        } for stat in stats]

        players_with_stats.append({
            "id": player.id,
            "first_name": player.first_name,
            "last_name": player.last_name,
            "position": player.position,
            "market_value": str(player.market_value),
            "stats": player_stats
        })

    return jsonify(players_with_stats)
