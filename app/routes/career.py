
from flask import Blueprint, request, jsonify
from app import get_dynamic_model, db

bp = Blueprint('goals', __name__, url_prefix='/goals')

def get_models(username, user_db_url):
    """Récupère les modèles dynamiques nécessaires"""
    models = get_dynamic_model(username, user_db_url)
    return (
        models.get('season_goals'),
        models.get('seasons'),
        models.get('user_profile')
    )

@bp.route('/', methods=['GET'])
def get_season_goals():
    """Récupérer les objectifs de la saison actuelle"""
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    user_id = request.args.get('user_id')
    
    if not all([username, user_db_url, user_id]):
        return jsonify({'error': 'username, user_db_url et user_id sont requis'}), 400
        
    SeasonGoal, Season, UserProfile = get_models(username, user_db_url)
    if not all([SeasonGoal, Season, UserProfile]):
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404

    # Récupérer la saison actuelle
    current_season = Season.query.order_by(Season.end_year.desc()).first()
    if not current_season:
        return jsonify({'error': 'Aucune saison trouvée'}), 404

    # Récupérer les objectifs
    goals = SeasonGoal.query.filter_by(
        user_id=user_id,
        season_id=current_season.id
    ).all()

    return jsonify([{
        'id': goal.id,
        'goal_text': goal.goal_text,
        'season_id': goal.season_id,
        'completed': goal.completed
    } for goal in goals]), 200

@bp.route('/', methods=['POST'])
def create_season_goals():
    """Créer de nouveaux objectifs pour la saison"""
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    data = request.json
    
    if not all([username, user_db_url]):
        return jsonify({'error': 'username et user_db_url sont requis'}), 400
    
    if not all([data.get('user_id'), data.get('goals')]):
        return jsonify({'error': 'user_id et goals sont requis'}), 400

    SeasonGoal, Season, UserProfile = get_models(username, user_db_url)
    if not all([SeasonGoal, Season, UserProfile]):
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404

    try:
        # Récupérer la saison actuelle
        current_season = Season.query.order_by(Season.end_year.desc()).first()
        if not current_season:
            return jsonify({'error': 'Aucune saison trouvée'}), 404

        # Créer les nouveaux objectifs
        new_goals = []
        for goal_text in data['goals']:
            goal = SeasonGoal(
                user_id=data['user_id'],
                season_id=current_season.id,
                goal_text=goal_text,
                completed=False
            )
            db.session.add(goal)
            new_goals.append(goal)

        db.session.commit()

        return jsonify({
            'message': 'Objectifs créés avec succès',
            'goals': [{
                'id': goal.id,
                'goal_text': goal.goal_text,
                'season_id': goal.season_id,
                'completed': goal.completed
            } for goal in new_goals]
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:goal_id>', methods=['PUT'])
def update_goal_status(goal_id):
    """Mettre à jour le statut d'un objectif"""
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    data = request.json
    
    if not all([username, user_db_url]):
        return jsonify({'error': 'username et user_db_url sont requis'}), 400

    SeasonGoal, _, _ = get_models(username, user_db_url)
    if not SeasonGoal:
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404

    try:
        goal = SeasonGoal.query.get(goal_id)
        if not goal:
            return jsonify({'error': 'Objectif non trouvé'}), 404

        if 'completed' in data:
            goal.completed = data['completed']

        db.session.commit()

        return jsonify({
            'message': 'Objectif mis à jour avec succès',
            'goal': {
                'id': goal.id,
                'goal_text': goal.goal_text,
                'season_id': goal.season_id,
                'completed': goal.completed
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
