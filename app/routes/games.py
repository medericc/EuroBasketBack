from flask import Blueprint, request, jsonify
from app import  db

bp = Blueprint('games', __name__, url_prefix='/games')

def get_models(username, user_db_url):
    """Récupère les modèles dynamiques nécessaires"""
    models = (username, user_db_url)
    return models.get('games'), models.get('game_stats')

@bp.route('/', methods=['GET'])
def get_games():
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    
    if not username or not user_db_url:
        return jsonify({'error': 'username et user_db_url sont requis'}), 400
        
    Game, _ = get_models(username, user_db_url)
    if not Game:
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404
        
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
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    data = request.json
    
    if not username or not user_db_url:
        return jsonify({'error': 'username et user_db_url sont requis'}), 400
        
    Game, GameStat = get_models(username, user_db_url)
    if not all([Game, GameStat]):
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404
        
    try:
        new_game = Game(
            season_id=data["season_id"],
            home_team_id=data["home_team_id"],
            away_team_id=data["away_team_id"],
            date=data["date"],
            home_score=data.get("home_score", 0),
            away_score=data.get("away_score", 0)
        )
        db.session.add(new_game)
        db.session.flush()  # Pour obtenir l'ID du nouveau match
        
        if "player_stats" in data:
            for stats in data["player_stats"]:
                new_stat = GameStat(
                    game_id=new_game.id,
                    player_id=stats["player_id"],
                    points=stats.get("points", 0),
                    rebounds=stats.get("rebounds", 0),
                    assists=stats.get("assists", 0),
                    minutes_played=stats.get("minutes_played", 0),
                    fgm=stats.get("fgm", 0),
                    fga=stats.get("fga", 0),
                    threepm=stats.get("threepm", 0),
                    threepa=stats.get("threepa", 0),
                    ftm=stats.get("ftm", 0),
                    fta=stats.get("fta", 0),
                    steals=stats.get("steals", 0),
                    blocks=stats.get("blocks", 0),
                    turnovers=stats.get("turnovers", 0)
                )
                db.session.add(new_stat)
                
        db.session.commit()
        return jsonify({"message": "Game created", "game_id": new_game.id}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@bp.route('/upcoming', methods=['GET'])
def get_upcoming_games():
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    team_id = request.args.get('team_id')
    
    Game, Team = get_models(username, user_db_url)
    
    current_date = datetime.now()
    
    query = Game.query.filter(
        Game.date >= current_date
    ).order_by(Game.date)
    
    if team_id:
        query = query.filter(
            (Game.home_team_id == team_id) | 
            (Game.away_team_id == team_id)
        )
    
    upcoming_games = query.limit(10).all()
    
    return jsonify([{
        "id": game.id,
        "date": game.date.isoformat(),
        "home_team": game.home_team.name,
        "away_team": game.away_team.name,
        "competition": "League"  # À adapter selon les compétitions
    } for game in upcoming_games])