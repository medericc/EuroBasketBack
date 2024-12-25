from flask import Blueprint, request, jsonify
from app import  db

bp = Blueprint('teams', __name__)

def get_team_model(username, user_db_url):
    """Récupère le modèle Team dynamique pour un utilisateur"""
    models = (username, user_db_url)
    return models.get('teams')
@bp.route('/teams', methods=['GET'])
def get_all_teams():
    """Récupère toutes les équipes de la table 'teams'"""
    teams = Team.query.all()  # Requête sur la table Team
    return jsonify([{
        'id': team.id,
        'name': team.name,
        'league_id': team.league_id,
        'budget': float(team.budget),  # Convertir Decimal en float
        'logo': team.logo
    } for team in teams]), 200

@bp.route('/teams/league/<int:league_id>', methods=['GET'])
def get_teams_by_league(league_id):
    """
    Récupère toutes les équipes pour une ligue spécifique.
    """
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')

    if not username or not user_db_url:
        return jsonify({'error': 'username et user_db_url sont requis'}), 400

    try:
        Team = ('teams', user_db_url)
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

    teams = Team.query.filter_by(league_id=league_id).all()
    if not teams:
        return jsonify({'message': f'Aucune équipe trouvée pour la ligue {league_id}'}), 404

    return jsonify([{
        'id': team.id,
        'name': team.name,
        'league_id': team.league_id,
        'budget': float(team.budget),
        'logo': team.logo
    } for team in teams]), 200

@bp.route('/teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
    """Récupère une équipe spécifique"""
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    
    if not username or not user_db_url:
        return jsonify({'error': 'username et user_db_url sont requis'}), 400
        
    Team = get_team_model(username, user_db_url)
    if not Team:
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404
        
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Équipe non trouvée'}), 404
        
    return jsonify({
        'id': team.id,
        'name': team.name,
        'league_id': team.league_id,
        'budget': float(team.budget),
        'logo': team.logo
    }), 200

@bp.route('/teams', methods=['POST'])
def create_team():
    """Crée une nouvelle équipe"""
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    data = request.get_json()
    
    if not username or not user_db_url:
        return jsonify({'error': 'username et user_db_url sont requis'}), 400
        
    Team = get_team_model(username, user_db_url)
    if not Team:
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404
        
    team = Team(
        name=data['name'],
        league_id=data['league_id'],
        budget=data.get('budget', 0),
        logo=data.get('logo')
    )
    
    db.session.add(team)
    db.session.commit()
    
    return jsonify({
        'id': team.id,
        'name': team.name,
        'league_id': team.league_id,
        'budget': float(team.budget),
        'logo': team.logo
    }), 201