# calcul de moyenne et autres
def calculate_ppg(total_points, games_played):
    """Calcule les points par match."""
    return round(total_points / games_played, 2) if games_played > 0 else 0

def calculate_rpg(total_rebounds, games_played):
    """Calcule les rebonds par match."""
    return round(total_rebounds / games_played, 2) if games_played > 0 else 0

def calculate_apg(total_assists, games_played):
    """Calcule les passes décisives par match."""
    return round(total_assists / games_played, 2) if games_played > 0 else 0
