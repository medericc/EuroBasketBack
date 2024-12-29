from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime, timedelta
from app.services.schedule_generator import generate_round_robin_schedule
from app.models import Team, UserProfile, Game, Season
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

        # Nouvelle route pour afficher le calendrier d'une saison
@bp.route('/schedule/<int:season_id>', methods=['GET'])
def get_schedule(season_id):
    """Récupère le calendrier d'une saison spécifique"""
    try:
        session = get_career_session()
        games = session.query(Game).filter_by(season_id=season_id).all()

        if not games:
            return jsonify({'message': f'Aucun match trouvé pour la saison {season_id}'}), 404

        schedule = [{
            'id': game.id,
            'season_id': game.season_id,
            'home_team_id': game.home_team_id,
            'away_team_id': game.away_team_id,
            'date': game.date.strftime('%Y-%m-%d'),
            'home_score': game.home_score,
            'away_score': game.away_score
        } for game in games]

        return jsonify(schedule), 200

    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération du calendrier: {str(e)}'}), 500
    finally:
        session.close()

# Nouvelle route pour générer le calendrier
@bp.route('/schedule/create', methods=['POST'])
def create_season_schedule():
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    data = request.json

    Season, Team = get_models(username, user_db_url)

    season = Season.query.get(data['season_id'])
    if not season:
        return jsonify({"error": "Saison non trouvée"}), 404

    teams = Team.query.all()
    if not teams:
        return jsonify({"error": "Pas d'équipes disponibles pour générer le calendrier"}), 404

    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')

    try:
        # Générer le calendrier
        schedule = generate_season_schedule(data['season_id'], teams, start_date)

        # Log des matchs avant insertion
        for game in schedule:
            print(f"Insertion prévue : {game}")

        # Enregistrer dans la base de données
        for game in schedule:
            new_game = Game(**game)
            db.session.add(new_game)

        db.session.commit()
        return jsonify({"message": "Calendrier généré avec succès"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@bp.route('/<int:team_id>/players', methods=['GET'])
def get_players_by_team(team_id):
    """Récupère tous les joueurs d'une équipe spécifique"""
    try:
        session = get_career_session()
        players = session.query(Player).filter_by(team_id=team_id).all()
        
        if not players:
            return jsonify({'message': 'Aucun joueur trouvé pour cette équipe'}), 404

        players_data = [{
            'id': player.id,
            'name': player.name,
            'position': player.position,
            'number': player.number,
            'stats': player.stats
        } for player in players]

        return jsonify(players_data), 200

    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération des joueurs: {str(e)}'}), 500
    finally:
        session.close()

@bp.route('/<int:team_id>/matches', methods=['GET'])
def get_matches_by_team(team_id):
    """Récupère tous les matchs pour une équipe spécifique"""
    try:
        session = get_career_session()
        matches = session.query(Game).filter(
            (Game.home_team_id == team_id) | (Game.away_team_id == team_id)
        ).all()

        if not matches:
            return jsonify({'message': 'Aucun match trouvé pour cette équipe'}), 404

        matches_data = [{
            'id': match.id,
            'season_id': match.season_id,
            'home_team_id': match.home_team_id,
            'away_team_id': match.away_team_id,
            'date': match.date.strftime('%Y-%m-%d'),
            'home_score': match.home_score,
            'away_score': match.away_score
        } for match in matches]

        return jsonify(matches_data), 200

    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération des matchs: {str(e)}'}), 500
    finally:
        session.close()


@bp.route('/games', methods=['POST', 'OPTIONS'])
@cross_origin()  # Ajouter CORS support
def create_schedule():
    if request.method == 'OPTIONS':
        return '', 204  # Handle OPTIONS request for CORS

    try:
        data = request.get_json()
        
        # Validation des données
        if not all(key in data for key in ['season_id', 'start_date']):
            return jsonify({'error': 'season_id et start_date sont requis'}), 400

        session = get_career_session()  # Utiliser la session career
        
        season = session.query(Season).get(data['season_id'])
        if not season:
            return jsonify({'error': 'Saison non trouvée'}), 404

        teams = session.query(Team).all()
        if len(teams) < 2:
            return jsonify({'error': 'Il faut au moins 2 équipes'}), 400

        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        
        # Génération du calendrier
        schedule = generate_round_robin_schedule(
            teams=teams,
            season_id=data['season_id'],
            start_date=start_date
        )

        # Sauvegarde des matchs
        for game_data in schedule:
            game = Game(**game_data)
            session.add(game)

        session.commit()

        return jsonify({
            'success': True,
            'message': f'{len(schedule)} matchs créés avec succès',
            'matches_count': len(schedule),
            'games': schedule
        }), 201

    except Exception as e:
        if session:
            session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        if session:
            session.close()