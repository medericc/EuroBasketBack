# fonctions génériques

def format_currency(value):
    """Formate un nombre décimal en monnaie avec deux décimales."""
    return f"{value:,.2f} €"

def validate_request_data(data, required_fields):
    """Valide que toutes les clés nécessaires sont présentes dans les données."""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing fields: {', '.join(missing_fields)}")
