from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.models import Team, UserProfile
from flask_cors import cross_origin
# Modifier le nom du blueprint ici pour éviter le conflit
bp = Blueprint('teams_career', __name__, url_prefix='/career/teams')

def get_career_session():
    """Helper function to create a session for career database"""
    db_url_prefix = os.getenv('DB_URL_PREFIX')
    career_db_name = "career_basket"
    career_db_url = f"{db_url_prefix}{career_db_name}"
    engine = create_engine(career_db_url)
    Session = sessionmaker(bind=engine)
    return Session()
def get_career_session():
    """Helper function to create a session for career database"""
    db_url_prefix = os.getenv('DB_URL_PREFIX')
    career_db_name = "career_basket"
    career_db_url = f"{db_url_prefix}{career_db_name}"
    engine = create_engine(career_db_url)
    Session = sessionmaker(bind=engine)
    return Session()

@bp.route('/', methods=['GET'])
def get_all_teams():
    """Récupère toutes les équipes"""
    try:
        session = get_career_session()
        teams = session.query(Team).all()
        
        teams_data = [{
            'id': team.id,
            'name': team.name,
            'league_id': team.league_id,
            'budget': float(team.budget) if team.budget else 0,
            'logo': team.logo
        } for team in teams]

        return jsonify(teams_data), 200

    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération des équipes: {str(e)}'}), 500
    finally:
        session.close()

@bp.route('/league/<int:league_id>', methods=['GET'])
def get_teams_by_league(league_id):
    """Récupère toutes les équipes pour une ligue spécifique"""
    try:
        session = get_career_session()
        teams = session.query(Team).filter_by(league_id=league_id).all()
        
        if not teams:
            return jsonify({'message': f'Aucune équipe trouvée pour la ligue {league_id}'}), 404

        teams_data = [{
            'id': team.id,
            'name': team.name,
            'league_id': team.league_id,
            'budget': float(team.budget) if team.budget else 0,
            'logo': team.logo
        } for team in teams]

        return jsonify(teams_data), 200

    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération des équipes: {str(e)}'}), 500
    finally:
        session.close()

@bp.route('/<int:team_id>', methods=['GET'])
def get_team(team_id):
    """Récupère une équipe spécifique"""
    try:
        session = get_career_session()
        team = session.query(Team).get(team_id)
        
        if not team:
            return jsonify({'error': 'Équipe non trouvée'}), 404

        return jsonify({
            'id': team.id,
            'name': team.name,
            'league_id': team.league_id,
            'budget': float(team.budget) if team.budget else 0,
            'logo': team.logo
        }), 200

    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération de l\'équipe: {str(e)}'}), 500
    finally:
        session.close()


@bp.route('/assign-team', methods=['POST', 'OPTIONS'])
@cross_origin()  # Permet les requêtes CORS pour cette route
def assign_team_to_user():
    """
    Assigne une équipe à un utilisateur.
    Reçoit `user_id` et `team_id` dans le corps de la requête.
    """
    if request.method == 'OPTIONS':
        return '', 204  # Réponse pour les pré-requêtes CORS

    session = get_career_session()

    try:
        # Parse les données JSON envoyées par le client
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Données requises manquantes'}), 400

        user_id = data.get('user_id')
        team_id = data.get('team_id')

        if not user_id or not team_id:
            return jsonify({'error': 'user_id et team_id sont requis'}), 400

        # Vérifier si l'utilisateur existe
        user = session.query(UserProfile).get(user_id)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404

        # Vérifier si l'équipe existe
        team = session.query(Team).get(team_id)
        if not team:
            return jsonify({'error': 'Équipe non trouvée'}), 404

        # Assignation de l'équipe à l'utilisateur
        user.team_id = team_id
        session.commit()

        # Construire une réponse détaillée
        return jsonify({
            'message': 'Équipe assignée avec succès',
            'user': {
                'id': user.id,
                'user_name': user.user_name,
                'team': {
                    'id': team.id,
                    'name': team.name,
                    'league_id': team.league_id,
                    'budget': float(team.budget) if team.budget else 0,
                    'logo': team.logo
                }
            }
        }), 200

    except Exception as e:
        session.rollback()  # Annuler les changements en cas d'erreur
        return jsonify({'error': f'Erreur lors de l\'assignation de l\'équipe: {str(e)}'}), 500

    finally:
        session.close()  # Toujours fermer la session