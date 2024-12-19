# gerer les matchs 
from flask import Blueprint, request, jsonify
from app.models import Game, GameStat
from app import db
bp = Blueprint('games', __name__, url_prefix='/games')

@bp.route('/', methods=['GET'])
def get_games():
    games = Game.query.all()
    return jsonify([{
        "id": game.id,
        "season_id": game.season_id,
        "home_team_id": game.home_team_id,
        "away_team_id": game.away_team_id,
        "date": game.date.isoformat(),
        "home_score": game.home_score,
        "away_score": game.away_score
    } for game in games])

@bp.route('/', methods=['POST'])
def create_game():
    data = request.json
    try:
        # Création du match
        new_game = Game(
            season_id=data['season_id'],
            home_team_id=data['home_team_id'],
            away_team_id=data['away_team_id'],
            date=data['date'],
            home_score=data.get('home_score', 0),
            away_score=data.get('away_score', 0)
        )
        db.session.add(new_game)
        db.session.flush()  # Permet d'obtenir l'ID du match avant la validation finale

        # Ajout des statistiques des joueurs
        player_stats = data.get('player_stats', [])
        for stats in player_stats:
            game_stat = GameStat(
                game_id=new_game.id,
                player_id=stats['player_id'],
                points=stats.get('points', 0),
                rebounds=stats.get('rebounds', 0),
                assists=stats.get('assists', 0),
                minutes_played=stats.get('minutes_played', 0),
                fgm=stats.get('fgm', 0),
                fga=stats.get('fga', 0),
                threepm=stats.get('threepm', 0),
                threepa=stats.get('threepa', 0),
                ftm=stats.get('ftm', 0),
                fta=stats.get('fta', 0),
                steals=stats.get('steals', 0),
                blocks=stats.get('blocks', 0),
                turnovers=stats.get('turnovers', 0)
            )
            db.session.add(game_stat)

        db.session.commit()
        return jsonify({"message": "Game and player stats created"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@bp.route('/<int:id>', methods=['GET'])
def get_game_details(id):
    game = Game.query.get_or_404(id)
    game_stats = GameStat.query.filter_by(game_id=id).all()
    return jsonify({
        "id": game.id,
        "season_id": game.season_id,
        "home_team_id": game.home_team_id,
        "away_team_id": game.away_team_id,
        "date": game.date.isoformat(),
        "home_score": game.home_score,
        "away_score": game.away_score,
        "player_stats": [{
            "player_id": stat.player_id,
            "points": stat.points,
            "rebounds": stat.rebounds,
            "assists": stat.assists,
            "minutes_played": stat.minutes_played,
            "fgm": stat.fgm,
            "fga": stat.fga,
            "threepm": stat.threepm,
            "threepa": stat.threepa,
            "ftm": stat.ftm,
            "fta": stat.fta,
            "steals": stat.steals,
            "blocks": stat.blocks,
            "turnovers": stat.turnovers
        } for stat in game_stats]
    })

@bp.route('/<int:id>', methods=['PUT'])
def update_game_scores(id):
    data = request.json
    try:
        game = Game.query.get_or_404(id)
        game.home_score = data.get('home_score', game.home_score)
        game.away_score = data.get('away_score', game.away_score)
        db.session.commit()
        return jsonify({"message": "Game scores updated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@bp.route('/simulate', methods=['POST'])
def simulate_game():
    data = request.json
    # Simulation logique basique
    home_score = data.get('home_score', 80)  # Exemple par défaut
    away_score = data.get('away_score', 75)
    return jsonify({
        "home_team_id": data['home_team_id'],
        "away_team_id": data['away_team_id'],
        "home_score": home_score,
        "away_score": away_score,
        "message": "Game simulated"
    }), 200
