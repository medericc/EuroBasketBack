from flask import Blueprint, request, jsonify
from app.models import UserProfile
import jwt
import datetime
from app import db

# Utilisez une clé sécurisée, idéalement chargée depuis les variables d'environnement
SECRET_KEY = "your_secret_key"

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    """Connexion d'un utilisateur via son email."""
    data = request.get_json()

    if not data or not data.get('email'):
        return jsonify({'error': 'Email est requis.'}), 400

    # Vérifier si l'utilisateur existe
    user = UserProfile.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé.'}), 404

    try:
        # Générer un token JWT pour l'utilisateur
        token = jwt.encode(
            {
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            },
            SECRET_KEY,
            algorithm='HS256'
        )

        return jsonify({
            'message': 'Connexion réussie.',
            'token': token,
            'user': {
                'id': user.id,
                'user_name': user.user_name,
                'email': user.email,
                'team_id': user.team_id  # Ajout de team_id dans la réponse
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Erreur lors de la génération du token.'}), 500
@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Récupérer les informations de l'utilisateur par ID."""
    user = UserProfile.query.get(user_id)
    if not user:
        return jsonify({'error': 'Utilisateur non trouvé.'}), 404

    # Construire la réponse JSON avec toutes les données nécessaires
    return jsonify({
        'id': user.id,
        'username': user.user_name,
        'email': user.email,
        'team_id': user.team_id  # Vérifie que ce champ est bien inclus
    }), 200
