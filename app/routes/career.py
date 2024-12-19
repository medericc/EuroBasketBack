from flask import Blueprint, request, jsonify
from app.models import UserProfile, Season, TeamSeason
from app import db
bp = Blueprint('career', __name__, url_prefix='/career')

# Obtenir les détails de la carrière de l'entraîneur
@bp.route('/', methods=['GET'])
def get_career_details():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user_profile = UserProfile.query.get(user_id)
    if not user_profile:
        return jsonify({"error": "User not found"}), 404

    team_seasons = TeamSeason.query.filter_by(team_id=user_profile.team_id).all()
    career_details = {
        "user_name": user_profile.user_name,
        "email": user_profile.email,
        "team": user_profile.team.name,
        "team_seasons": [{
            "season_id": ts.season_id,
            "wins": ts.wins,
            "losses": ts.losses,
            "budget_remaining": str(ts.budget_remaining)
        } for ts in team_seasons]
    }

    return jsonify(career_details), 200

# Avancer dans la carrière (saison suivante)
@bp.route('/advance', methods=['POST'])
def advance_career():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user_profile = UserProfile.query.get(user_id)
    if not user_profile:
        return jsonify({"error": "User not found"}), 404

    current_season = db.session.query(Season).order_by(Season.end_year.desc()).first()
    next_season = Season(start_year=current_season.end_year + 1, end_year=current_season.end_year + 2)
    db.session.add(next_season)

    team_season = TeamSeason(
        team_id=user_profile.team_id,
        season_id=next_season.id,
        budget_remaining=user_profile.team.budget
    )
    db.session.add(team_season)
    db.session.commit()

    return jsonify({"message": "Career advanced to the next season"}), 200

# Ajouter des objectifs pour la saison
@bp.route('/goals', methods=['POST'])
def add_season_goals():
    data = request.json
    user_id = data.get('user_id')
    goals = data.get('goals')

    if not user_id or not goals:
        return jsonify({"error": "User ID and goals are required"}), 400

    user_profile = UserProfile.query.get(user_id)
    if not user_profile:
        return jsonify({"error": "User not found"}), 404

    current_season = db.session.query(Season).order_by(Season.end_year.desc()).first()

    # Simulez une table pour stocker les objectifs
    # Par exemple, une table `SeasonGoals` avec `user_id`, `season_id` et `goal_text`.

    # Exemple de sauvegarde d'objectifs
    for goal in goals:
        new_goal = SeasonGoal(user_id=user_id, season_id=current_season.id, goal_text=goal)
        db.session.add(new_goal)

    db.session.commit()

    return jsonify({"message": "Goals added for the season"}), 201

# Récupérer les objectifs actuels
@bp.route('/goals', methods=['GET'])
def get_season_goals():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user_profile = UserProfile.query.get(user_id)
    if not user_profile:
        return jsonify({"error": "User not found"}), 404

    current_season = db.session.query(Season).order_by(Season.end_year.desc()).first()
    goals = SeasonGoal.query.filter_by(user_id=user_id, season_id=current_season.id).all()

    return jsonify([{
        "id": goal.id,
        "goal_text": goal.goal_text
    } for goal in goals]), 200
