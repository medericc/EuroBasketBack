from datetime import datetime

def validate_finance_data(data):
    """
    Valide les données financières entrantes.
    
    Args:
        data (dict): Données financières à valider
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    required_fields = ['type', 'amount', 'date']
    
    # Vérifier les champs requis
    for field in required_fields:
        if field not in data:
            return False, f"Le champ '{field}' est requis"
            
    # Valider le type
    if data['type'] not in ['revenue', 'expense']:
        return False, "Le type doit être 'revenue' ou 'expense'"
        
    # Valider le montant
    try:
        amount = float(data['amount'])
        if amount < 0:
            return False, "Le montant ne peut pas être négatif"
    except ValueError:
        return False, "Le montant doit être un nombre valide"
        
    # Valider la date
    try:
        datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        return False, "Format de date invalide. Utilisez le format ISO 8601"
        
    return True, ""