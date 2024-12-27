from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.models import Team, UserProfile

bp = Blueprint('teams', __name__)

def get_career_session():
    """Helper function to create a session for career database"""
    db_url_prefix = os.getenv('DB_URL_PREFIX')
    career_db_name = "career_basket"
    career_db_url = f"{db_url_prefix}{career_db_name}"
    engine = create_engine(career_db_url)
    Session = sessionmaker(bind=engine)
    return Session()

@bp.route('/teams/league/<int:league_id>', methods=['GET'])
def get_teams_by_league(league_id):
    """
    Récupère toutes les équipes pour une ligue spécifique depuis la base career_basket.
    """
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

@bp.route('/users/<int:user_id>/team', methods=['PUT'])
def update_user_team(user_id):
    """
    Met à jour l'équipe d'un utilisateur dans la base career_basket.
    """
    try:
        session = get_career_session()
        data = request.get_json()

        if not data or 'team_id' not in data:
            return jsonify({'error': 'team_id est requis'}), 400

        # Vérifier si l'utilisateur existe
        user = session.query(UserProfile).get(user_id)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404

        # Vérifier si l'équipe existe
        team = session.query(Team).get(data['team_id'])
        if not team:
            return jsonify({'error': 'Équipe non trouvée'}), 404

        # Mettre à jour l'équipe de l'utilisateur
        user.team_id = team.id
        session.commit()

        return jsonify({
            'message': 'Équipe mise à jour avec succès',
            'user': {
                'id': user.id,
                'user_name': user.user_name,
                'email': user.email,
                'team': {
                    'id': team.id,
                    'name': team.name,
                    'logo': team.logo
                }
            }
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({'error': f'Erreur lors de la mise à jour: {str(e)}'}), 500
    
    finally:
        session.close()