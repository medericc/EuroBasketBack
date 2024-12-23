# transfer_periods.py
from datetime import datetime
from enum import Enum

class TransferPeriod(Enum):
    SUMMER = "SUMMER"
    WINTER = "WINTER"

def is_transfer_window_open(current_date):
    """
    Vérifie si une période de transfert est ouverte
    Été : 1er juillet - 31 août
    Hiver : 1er janvier - 31 janvier
    """
    month = current_date.month
    day = current_date.day
    
    if (month == 7 or month == 8):
        return TransferPeriod.SUMMER
    elif month == 1:
        return TransferPeriod.WINTER
    return None

# Mise à jour de la route transfer
@bp.route('/', methods=['POST'])
def create_transfer():
    # ... code existant ...
    
    current_date = datetime.strptime(data['date'], '%Y-%m-%d')
    transfer_window = is_transfer_window_open(current_date)
    
    if not transfer_window:
        return jsonify({
            "error": "Les transferts ne sont possibles que pendant les périodes de transfert"
        }), 400
