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

@bp.route('/', methods=['POST', 'OPTIONS'])
def create_game():
    data = request.json
    logger.info("Requête reçue pour créer un jeu.")
    
    try:
        # Journal des données reçues
        logger.debug(f"Données reçues : {data}")
        
        # Vérification si le match existe déjà
        existing_game = Game.query.filter_by(
            season_id=data.get("season_id"),
            home_team_id=data.get("home_team_id"),
            away_team_id=data.get("away_team_id"),
            date=data.get("date")
        ).first()

        if existing_game:
            logger.warning(f"Match déjà existant : {existing_game}")
            return jsonify({"message": "Match already exists"}), 400

        # Création du match
        new_game = Game(
            season_id=data["season_id"],
            home_team_id=data["home_team_id"],
            away_team_id=data["away_team_id"],
            date=data["date"],
            home_score=data.get("home_score", 0),
            away_score=data.get("away_score", 0)
        )
        db.session.add(new_game)
        db.session.commit()
        logger.info(f"Nouveau match créé avec succès : {new_game}")

        # Ajout des statistiques des joueurs
        if "player_stats" in data:
            for stats in data["player_stats"]:
                logger.debug(f"Ajout des statistiques pour le joueur {stats['player_id']}")
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
                    turnovers=stats.get("turnovers", 0),
                )
                db.session.add(new_stat)

            db.session.commit()
            logger.info(f"Statistiques des joueurs ajoutées pour le match {new_game.id}")

        return jsonify({"message": "Game created successfully", "game_id": new_game.id}), 201

    except Exception as e:
        logger.error(f"Erreur lors de la création du match : {e}", exc_info=True)
        db.session.rollback()
        return jsonify({"message": "An error occurred while creating the game"}), 500


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
