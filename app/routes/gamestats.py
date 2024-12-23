from flask import Blueprint, request, jsonify
from app import get_dynamic_model, db
from flask import current_app as app
from app.models import GameStat, PlayerStat, Player, Season, Game

bp = Blueprint('gamestats', __name__)

@bp.route('/update_player_stats', methods=['POST'])
def update_player_stats():
    try:
        # Récupérer les données envoyées dans la requête
        game_stats_data = request.json.get('game_stats', [])
        season_id = request.json.get('season_id')

        if not game_stats_data or not season_id:
            return jsonify({"error": "Missing game_stats data or season_id"}), 400

        for stat in game_stats_data:
            game_id = stat.get('game_id')
            player_id = stat.get('player_id')
            points = stat.get('points', 0)
            rebounds = stat.get('rebounds', 0)
            assists = stat.get('assists', 0)
            minutes_played = stat.get('minutes_played', 0)
            fgm = stat.get('fgm', 0)
            fga = stat.get('fga', 0)
            threepm = stat.get('threepm', 0)
            threepa = stat.get('threepa', 0)
            ftm = stat.get('ftm', 0)
            fta = stat.get('fta', 0)
            steals = stat.get('steals', 0)
            blocks = stat.get('blocks', 0)
            turnovers = stat.get('turnovers', 0)

            # Vérifier si le jeu existe avant d'ajouter des statistiques
            game = Game.query.get(game_id)
            if not game:
                raise ValueError(f"Le jeu avec l'ID {game_id} n'existe pas.")

            # Vérifier si les statistiques de ce joueur existent déjà pour cette saison
            player_stat = PlayerStat.query.filter_by(player_id=player_id, season_id=season_id).first()

            if player_stat:
                # Si les stats existent, on les met à jour
                player_stat.games_played += 1
                player_stat.ppg += points
                player_stat.apg += assists
                player_stat.rpg += rebounds
                player_stat.minutes_played += minutes_played
                player_stat.fgm += fgm
                player_stat.fga += fga
                player_stat.threepm += threepm
                player_stat.threepa += threepa
                player_stat.ftm += ftm
                player_stat.fta += fta
                player_stat.steals += steals
                player_stat.blocks += blocks
                player_stat.turnovers += turnovers
            else:
                # Si les stats n'existent pas, on les crée
                player_stat = PlayerStat(
                    player_id=player_id,
                    season_id=season_id,
                    games_played=1,
                    ppg=points,
                    apg=assists,
                    rpg=rebounds,
                    minutes_played=minutes_played,
                    fgm=fgm,
                    fga=fga,
                    threepm=threepm,
                    threepa=threepa,
                    ftm=ftm,
                    fta=fta,
                    steals=steals,
                    blocks=blocks,
                    turnovers=turnovers
                )
                db.session.add(player_stat)

            # Enregistrer les statistiques du match dans la table GameStat
            game_stat = GameStat(
                game_id=game.id,  # Utilisation de game.id après la vérification
                player_id=player_id,
                points=points,
                rebounds=rebounds,
                assists=assists,
                minutes_played=minutes_played,
                fgm=fgm,
                fga=fga,
                threepm=threepm,
                threepa=threepa,
                ftm=ftm,
                fta=fta,
                steals=steals,
                blocks=blocks,
                turnovers=turnovers
            )
            db.session.add(game_stat)

        # Commit les changements dans la base de données
        db.session.commit()

        return jsonify({"message": "Player stats updated successfully."}), 200

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500
