from flask import Blueprint, request, jsonify
from app.models import Event, Player, Team
from app import db
# Définition du blueprint pour les routes des événements
bp = Blueprint('events', __name__)

@bp.route('/events', methods=['GET'])
def get_events():
    """
    Récupérer tous les événements.
    Retourne :
        - Une liste d'objets JSON représentant les événements.
    """
    try:
        events = Event.query.all()

        # Transformer les objets Event en dictionnaires JSON
        events_data = [
            {
                "id": event.id,
                "description": event.description,
                "date": event.date,
                "type": event.type,
                "player_id": event.player_id,
                "team_id": event.team_id
            } for event in events
        ]

        return jsonify({
            "success": True,
            "data": events_data
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@bp.route('/events', methods=['POST'])
def create_event():
    """
    Ajouter un événement à un joueur ou une équipe.
    Corps attendu (JSON) :
        - description : Description de l'événement
        - date : Date de l'événement
        - type : Type d'événement (ex. "blessure", "record", etc.)
        - player_id : ID du joueur (facultatif)
        - team_id : ID de l'équipe (facultatif)
    """
    data = request.json

    try:
        new_event = Event(
            description=data['description'],
            date=data['date'],
            type=data['type'],
            player_id=data.get('player_id'),
            team_id=data.get('team_id')
        )
        db.session.add(new_event)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Event created",
            "event": {
                "id": new_event.id,
                "description": new_event.description,
                "date": new_event.date,
                "type": new_event.type,
                "player_id": new_event.player_id,
                "team_id": new_event.team_id
            }
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400


@bp.route('/events/player/<int:player_id>', methods=['GET'])
def get_events_by_player(player_id):
    """
    Récupérer l'historique des événements d'un joueur.
    Paramètre :
        - player_id : ID du joueur
    Retourne :
        - Une liste d'objets JSON représentant les événements du joueur.
    """
    try:
        events = Event.query.filter_by(player_id=player_id).all()

        events_data = [
            {
                "id": event.id,
                "description": event.description,
                "date": event.date,
                "type": event.type,
                "team_id": event.team_id
            } for event in events
        ]

        return jsonify({
            "success": True,
            "data": events_data
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
