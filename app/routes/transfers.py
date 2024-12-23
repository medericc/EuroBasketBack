from flask import Blueprint, request, jsonify
from app import get_dynamic_model, db

bp = Blueprint('transfers', __name__, url_prefix='/transfers')

def get_models(username, user_db_url):
    """Récupère les modèles dynamiques nécessaires"""
    models = get_dynamic_model(username, user_db_url)
    return models.get('transfers'), models.get('players'), models.get('teams')

@bp.route('/', methods=['GET'])
def get_transfers():
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    
    if not username or not user_db_url:
        return jsonify({'error': 'username et user_db_url sont requis'}), 400
        
    Transfer, _, _ = get_models(username, user_db_url)
    if not Transfer:
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404
        
    transfers = Transfer.query.all()
    return jsonify([{
        "id": transfer.id,
        "player_id": transfer.player_id,
        "from_team_id": transfer.from_team_id,
        "to_team_id": transfer.to_team_id,
        "transfer_fee": str(transfer.transfer_fee),
        "date": transfer.date.isoformat()
    } for transfer in transfers])

@bp.route('/', methods=['POST'])
def create_transfer():
    username = request.args.get('username')
    user_db_url = request.args.get('user_db_url')
    data = request.json
    
    if not username or not user_db_url:
        return jsonify({'error': 'username et user_db_url sont requis'}), 400
        
    Transfer, Player, Team = get_models(username, user_db_url)
    if not all([Transfer, Player, Team]):
        return jsonify({'error': 'Tables de carrière non trouvées'}), 404
        
    try:
        new_transfer = Transfer(
            player_id=data['player_id'],
            from_team_id=data.get('from_team_id'),
            to_team_id=data['to_team_id'],
            transfer_fee=data['transfer_fee'],
            date=data['date']
        )
        
        # Mise à jour de l'équipe du joueur
        player = Player.query.get(data['player_id'])
        if player:
            player.team_id = data['to_team_id']
            
        db.session.add(new_transfer)
        db.session.commit()
        
        return jsonify({"message": "Transfer created"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400