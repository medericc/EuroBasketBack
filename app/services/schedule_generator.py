from datetime import datetime, timedelta
from typing import List, Dict
from app.models import Team, Game

def generate_round_robin_schedule(teams: List[Team], season_id: int, start_date: datetime) -> List[Dict]:
    """
    Génère un calendrier aller-retour où toutes les équipes jouent le même jour.
    """
    if len(teams) % 2 != 0:
        raise ValueError("Le nombre d'équipes doit être pair")

    games = []
    teams = list(teams)  # Copie de la liste pour ne pas modifier l'original
    n = len(teams)
    mid = n // 2
    current_date = start_date

    # Nombre de journées pour un tour complet = n-1 (où n est le nombre d'équipes)
    for round_num in range(2):  # 2 tours (aller-retour)
        for day in range(n - 1):
            # Matchs de la journée
            day_games = []
            for i in range(mid):
                home = teams[i]
                away = teams[n - 1 - i]
                
                # Pour les matchs retour, on inverse domicile/extérieur
                if round_num == 1:
                    home, away = away, home

                game = {
                    'season_id': season_id,
                    'home_team_id': home.id,
                    'away_team_id': away.id,
                    'date': current_date,
                    'home_score': 0,
                    'away_score': 0
                }
                day_games.append(game)
            
            games.extend(day_games)
            current_date += timedelta(days=7)  # Prochain match dans 7 jours

            # Rotation des équipes (algorithme de Berger)
            teams = [teams[0]] + [teams[-1]] + teams[1:-1]

    return games