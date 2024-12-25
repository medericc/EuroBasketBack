# events/routes.py
from flask import Blueprint, request, jsonify
from app import  db
# from .utils import generate_injury_event, generate_performance_event
from datetime import datetime

bp = Blueprint('events', __name__, url_prefix='/events')

def get_models(username, user_db_url):
    """Récupère les modèles dynamiques nécessaires"""
    models = (username, user_db_url)
    return (
        models.get('events'),
        models.get('players'),
        models.get('teams')
    )

@bp.route('/', methods=['GET'])
def get_events():
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    
    if not all([username, user_db_url]):
        return jsonify({'error': 'username et user_db_url sont requis'}), 400
        
    Event, _, _ = get_models(username, user_db_url)
    if not Event:
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404

    events = Event.query.order_by(Event.date.desc()).all()
    return jsonify([{
        'id': event.id,
        'description': event.description,
        'date': event.date.isoformat(),
        'type': event.type,
        'player_id': event.player_id,
        'team_id': event.team_id
    } for event in events]), 200

@bp.route('/player/<int:player_id>', methods=['GET'])
def get_player_events(player_id):
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    
    if not all([username, user_db_url]):
        return jsonify({'error': 'username et user_db_url sont requis'}), 400
        
    Event, Player, _ = get_models(username, user_db_url)
    if not all([Event, Player]):
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404

    player = Player.query.get(player_id)
    if not player:
        return jsonify({'error': 'Joueur non trouvé'}), 404

    events = Event.query.filter_by(player_id=player_id).order_by(Event.date.desc()).all()
    return jsonify([{
        'id': event.id,
        'description': event.description,
        'date': event.date.isoformat(),
        'type': event.type,
        'team_id': event.team_id
    } for event in events]), 200

@bp.route('/simulate-day', methods=['POST'])
def simulate_day_events():
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    data = request.json
    
    if not all([username, user_db_url]):
        return jsonify({'error': 'username et user_db_url sont requis'}), 400

    Event, Player, Team = get_models(username, user_db_url)
    if not all([Event, Player, Team]):
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404

    try:
        current_date = datetime.strptime(data['date'], '%Y-%m-%d')
        players = Player.query.all()
        new_events = []

        for player in players:
            # Simulation des blessures
            injury_event = generate_injury_event(player, current_date)
            if injury_event:
                event = Event(**injury_event)
                db.session.add(event)
                new_events.append(injury_event)

            # Simulation des performances exceptionnelles
            performance_event = generate_performance_event(player, current_date)
            if performance_event:
                event = Event(**performance_event)
                db.session.add(event)
                new_events.append(performance_event)

        db.session.commit()
        return jsonify({
            'message': 'Événements simulés avec succès',
            'events': new_events
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
