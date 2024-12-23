# events/utils.py
import random
from datetime import datetime, timedelta

def generate_injury_event(player, current_date):
    """Génère un événement de blessure aléatoire pour un joueur"""
    injury_chance = 0.05  # 5% de chance de blessure par jour
    if random.random() < injury_chance:
        injuries = [
            ("Entorse à la cheville", random.randint(7, 14)),
            ("Claquage musculaire", random.randint(10, 21)),
            ("Tendinite au genou", random.randint(5, 10)),
            ("Contracture", random.randint(3, 7)),
            ("Élongation", random.randint(5, 12))
        ]
        
        injury, days = random.choice(injuries)
        return {
            'description': f"{player.first_name} {player.last_name} : {injury}",
            'date': current_date,
            'type': 'injury',
            'player_id': player.id,
            'team_id': player.team_id,
            'duration_days': days
        }
    return None

def generate_performance_event(player, current_date):
    """Génère un événement de performance exceptionnelle pour un joueur"""
    performance_chance = 0.1  # 10% de chance d'événement de performance
    if random.random() < performance_chance:
        performances = [
            f"Record personnel de points en carrière : {random.randint(30, 50)} pts",
            f"Triple-double exceptionnel",
            f"Record de passes décisives en un match : {random.randint(12, 18)}",
            f"Performance défensive remarquable avec {random.randint(5, 8)} contres",
            f"Match parfait aux lancers-francs"
        ]
        
        performance = random.choice(performances)
        return {
            'description': f"{player.first_name} {player.last_name} : {performance}",
            'date': current_date,
            'type': 'performance',
            'player_id': player.id,
            'team_id': player.team_id
        }
    return None
