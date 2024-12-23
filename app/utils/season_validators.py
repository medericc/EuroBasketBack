def validate_season_data(data):
    """
    Valide les données d'une saison.
    
    Args:
        data (dict): Données de la saison à valider
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    required_fields = ['start_year', 'end_year']
    
    # Vérifier les champs requis
    for field in required_fields:
        if field not in data:
            return False, f"Le champ '{field}' est requis"
    
    try:
        start_year = int(data['start_year'])
        end_year = int(data['end_year'])
        
        # Vérifier que l'année de fin est après l'année de début
        if end_year <= start_year:
            return False, "L'année de fin doit être supérieure à l'année de début"
            
        # Vérifier que la durée est d'un an
        if end_year - start_year != 1:
            return False, "La durée d'une saison doit être d'un an"
            
    except ValueError:
        return False, "Les années doivent être des nombres entiers valides"
        
    return True, ""