# schedule_generator.py
from datetime import datetime, timedelta
import random

def generate_season_schedule(season_id, teams, start_date, end_date):
    games = []
    current_date = start_date

    num_teams = len(teams)
    num_days = (num_teams - 1) * 2  # Aller + retour

    for day in range(num_days):
        for i in range(num_teams // 2):
            home_team = teams[i]
            away_team = teams[-(i + 1)]

            game = {
                'season_id': season_id,
                'home_team_id': home_team.id,
                'away_team_id': away_team.id,
                'date': current_date,
                'home_score': 0,
                'away_score': 0
            }

            # Vérifier si la date dépasse la limite
            if current_date > end_date:
                print(f"Tentative de planification après {end_date}: {game}")
                raise ValueError(f"Date {current_date} dépasse la plage autorisée.")

            games.append(game)

        # Passer à la prochaine journée
        current_date += timedelta(days=7)

    return games

# Mise à jour de la route season
@bp.route('/create_schedule', methods=['POST'])
def create_season_schedule():
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    data = request.json

    Season, Team = get_models(username, user_db_url)

    season = Season.query.get(data['season_id'])
    if not season:
        return jsonify({"error": "Saison non trouvée"}), 404

    teams = Team.query.all()
    if not teams:
        return jsonify({"error": "Pas d'équipes disponibles pour générer le calendrier"}), 404

    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')

    try:
        # Générer le calendrier
        schedule = generate_season_schedule(data['season_id'], teams, start_date)

        # Log des matchs avant insertion
        for game in schedule:
            print(f"Insertion prévue : {game}")

        # Enregistrer dans la base de données
        for game in schedule:
            new_game = Game(**game)
            db.session.add(new_game)

        db.session.commit()
        return jsonify({"message": "Calendrier généré avec succès"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
