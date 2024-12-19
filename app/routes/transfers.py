# transferts entre équipes
from flask import Blueprint, request, jsonify
from app.models import Transfer, db

bp = Blueprint('transfers', __name__, url_prefix='/transfers')

@bp.route('/', methods=['GET'])
def get_transfers():
    transfers = Transfer.query.all()
    return jsonify([{
        "id": transfer.id,
        "player_id": transfer.player_id,
        "from_team_id": transfer.from_team_id,
        "to_team_id": transfer.to_team_id,
        "transfer_fee": str(transfer.transfer_fee),
        "date": transfer.date
    } for transfer in transfers])

@bp.route('/', methods=['POST'])
def create_transfer():
    data = request.json
    try:
        new_transfer = Transfer(
            player_id=data['player_id'],
            from_team_id=data.get('from_team_id'),
            to_team_id=data['to_team_id'],
            transfer_fee=data['transfer_fee'],
            date=data['date']
        )
        db.session.add(new_transfer)
        db.session.commit()
        return jsonify({"message": "Transfer created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
@bp.route('/player/<int:player_id>', methods=['GET'])
def get_transfers_by_player(player_id):
    transfers = Transfer.query.filter_by(player_id=player_id).all()
    return jsonify([
        {
            "id": transfer.id,
            "from_team_id": transfer.from_team_id,
            "to_team_id": transfer.to_team_id,
            "transfer_fee": str(transfer.transfer_fee),
            "date": transfer.date.strftime('%Y-%m-%d')
        } for transfer in transfers
    ])