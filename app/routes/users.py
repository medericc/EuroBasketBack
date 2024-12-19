from flask import Blueprint, request, jsonify
from app.models import db, UserProfile, Team

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
def create_user():
    """
    Crée un nouvel utilisateur avec une équipe associée.
    """
    data = request.get_json()

    # Vérification des données
    if not data.get('user_name') or not data.get('email') or not data.get('team_id'):
        return jsonify({'error': 'user_name, email, et team_id sont requis.'}), 400

    # Vérification si l'équipe existe
    team = Team.query.get(data['team_id'])
    if not team:
        return jsonify({'error': 'Équipe non trouvée.'}), 404

    # Création de l'utilisateur
    user = UserProfile(
        user_name=data['user_name'],
        email=data['email'],
        team_id=team.id
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'Utilisateur créé avec succès.',
        'user': {
            'id': user.id,
            'user_name': user.user_name,
            'email': user.email,
            'team': {
                'id': team.id,
                'name': team.name
            }
        }
    }), 201


@users_bp.route('/users/<int:user_id>', methods=['PUT'])
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
