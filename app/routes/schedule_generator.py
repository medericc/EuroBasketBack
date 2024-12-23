# schedule_generator.py
from datetime import datetime, timedelta
import random

def generate_season_schedule(season_id, teams, start_date):
    """
    Génère le calendrier d'une saison complète
    """
    games = []
    current_date = start_date
    
    # Créer les matchs aller
    for home_team in teams:
        for away_team in teams:
            if home_team.id != away_team.id:
                # Éviter les matchs le même jour
                while is_date_occupied(current_date, games):
                    current_date += timedelta(days=1)
                
                # Créer le match aller
                games.append({
                    'season_id': season_id,
                    'home_team_id': home_team.id,
                    'away_team_id': away_team.id,
                    'date': current_date,
                    'home_score': 0,
                    'away_score': 0
                })
                
                current_date += timedelta(days=7)  # Prochain match dans une semaine
    
    # Créer les matchs retour (même logique avec dates différentes)
    return games

# Mise à jour de la route season
@bp.route('/create_schedule', methods=['POST'])
def create_season_schedule():
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    data = request.json
    
    Season, Team = get_models(username, user_db_url)
    
    teams = Team.query.all()
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    
    schedule = generate_season_schedule(
        data['season_id'],
        teams,
        start_date
    )
    
    try:
        for game in schedule:
            new_game = Game(**game)
            db.session.add(new_game)
        
        db.session.commit()
        return jsonify({"message": "Calendrier généré avec succès"}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
