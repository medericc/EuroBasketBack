from flask import Blueprint, request, jsonify
from app.models import  UserProfile, Team
from app import db
bp = Blueprint('users', __name__)

@bp.route('/users', methods=['POST'])
def create_user():
    """
    Crée un nouvel utilisateur sans associer d'équipe au départ.
    """
    data = request.get_json()

    # Vérification des données
    if not data.get('user_name') or not data.get('email'):
        return jsonify({'error': 'user_name et email sont requis.'}), 400

    # Création de l'utilisateur sans équipe
    user = UserProfile(
        user_name=data['user_name'],
        email=data['email'],
        team_id=None  # Pas d'équipe associée pour le moment
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'Utilisateur créé avec succès.',
        'user': {
            'id': user.id,
            'user_name': user.user_name,
            'email': user.email,
            'team': None  # Pas d'équipe associée
        }
    }), 201



@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user_team(user_id):
    """
    Met à jour l'équipe associée à un utilisateur.
    """
    data = request.get_json()

    # Vérification si l'utilisateur existe
    user = UserProfile.query.get(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé.'}), 404

    # Vérification si l'équipe existe
    if not data.get('team_id'):
        return jsonify({'error': 'team_id est requis.'}), 400

    team = Team.query.get(data['team_id'])
    if not team:
        return jsonify({'error': 'Équipe non trouvée.'}), 404

    # Mise à jour de l'équipe
    user.team_id = team.id
    db.session.commit()

    return jsonify({
        'message': 'Équipe mise à jour avec succès.',
        'user': {
            'id': user.id,
            'user_name': user.user_name,
            'email': user.email,
            'team': {
                'id': team.id,
                'name': team.name
            }
        }
    }), 200
