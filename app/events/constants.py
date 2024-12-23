# events/constants.py
EVENT_TYPES = {
    'INJURY': 'injury',
    'PERFORMANCE': 'performance',
    'TRANSFER': 'transfer',
    'ACHIEVEMENT': 'achievement',
    'TRAINING': 'training'
}

INJURY_TYPES = [
    {
        'name': 'Entorse à la cheville',
        'min_days': 7,
        'max_days': 14
    },
    {
        'name': 'Claquage musculaire',
        'min_days': 10,
        'max_days': 21
    },
    {
        'name': 'Tendinite au genou',
        'min_days': 5,
        'max_days': 10
    },
    {
        'name': 'Contracture',
        'min_days': 3,
        'max_days': 7
    },
    {
        'name': 'Élongation',
        'min_days': 5,
        'max_days': 12
    }
]

PERFORMANCE_TYPES = [
    'Record personnel de points',
    'Triple-double',
    'Record de passes décisives',
    'Performance défensive',
    'Match parfait aux lancers-francs'
]
