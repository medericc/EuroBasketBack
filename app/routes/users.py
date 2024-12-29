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

    # Vérification des données obligatoires
    if not data.get('user_name') or not data.get('email'):
        return jsonify({'error': 'Les champs user_name et email sont requis.'}), 400

    # Vérifie si l'utilisateur existe déjà (par exemple, avec l'email)
    existing_user = UserProfile.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'Un utilisateur avec cet email existe déjà.'}), 400

    # Création de l'utilisateur sans équipe
    user = UserProfile(
        user_name=data['user_name'],
        email=data['email'],
        # Peut être défini ou None
        team_id=None  # Pas d'équipe associée pour le moment
    )

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Erreur lors de la création de l'utilisateur : {str(e)}"}), 500

    # Retourne les détails de l'utilisateur créé
    return jsonify({
        'message': 'Utilisateur créé avec succès.',
        'user': {
            'id': user.id,
            'user_name': user.user_name,
            'email': user.email,
            'team': None  # Pas d'équipe associée pour l'instant
        }
    }), 201

@bp.route('/users/<int:user_id>/team', methods=['PUT'])
def assign_team(user_id):
    """
    Associe un utilisateur à une équipe dans la base `career_basket`.
    """
    # Charger l'URL de la base dynamique
    db_url_prefix = os.getenv('DB_URL_PREFIX')
    career_db_name = "career_basket"
    career_db_url = f"{db_url_prefix}{career_db_name}"

    # Créer un moteur SQLAlchemy pour la base `career_basket`
    engine = create_engine(career_db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Récupérer les données de la requête
        data = request.get_json()
        team_id = data.get('team_id')

        if not team_id:
            return jsonify({'error': 'team_id est requis.'}), 400

        # Rechercher l'utilisateur et l'équipe
        user = session.query(UserProfile).get(user_id)
        if not user:
            return jsonify({'error': 'Utilisateur introuvable.'}), 404

        team = session.query(Team).get(team_id)
        if not team:
            return jsonify({'error': 'Équipe introuvable.'}), 404

        # Associer l'équipe à l'utilisateur
        user.team_id = team_id
        session.commit()

        return jsonify({
            'message': 'Équipe associée avec succès.',
            'user': {
                'id': user.id,
                'user_name': user.user_name,
                'email': user.email,
                'team_id': user.team_id,
                'team_name': team.name
            }
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({'error': f"Erreur lors de l'association de l'équipe : {str(e)}"}), 500

    finally:
        session.close()

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

@bp.route('/users/<int:user_id>', methods=['GET', 'PUT'])
def handle_user(user_id):
    """
    Gestion des opérations utilisateur :
    - GET : Récupère les informations de l'utilisateur.
    - PUT : Met à jour l'équipe associée à un utilisateur.
    """
    if request.method == 'GET':
         # Vérification si l'utilisateur existe
        user = UserProfile.query.get(user_id)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé.'}), 404

    # Construction de la réponse
        return jsonify({
            'id': user.id,
            'username': user.user_name,
            'email': user.email,
           
            'team': {
                'id': user.team.id if user.team else None,
                'name': user.team.name if user.team else None,
                'logo': user.team.logo if user.team else None,
                'budget': user.team.budget if user.team else None
            } if user.team else None
        }), 200

    elif request.method == 'PUT':
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
                    'name': team.name,
                    'budget':team.budget,
                }
            }
        }), 200
