from flask import Blueprint, jsonify, abort, make_response, request
from app import db

from app.models.board import Board
from app.routes.routes_helper import get_valid_item_by_id

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=['GET'])
def handle_boards():
    name_query = request.args.get("name")
    if name_query:
        boards = Board.query.filter_by(name=name_query)
    else:
        boards = Board.query.all()

    boards_response = []
    for board in boards :
        boards_response.append(board.to_dict())
    return jsonify(boards_response), 200


@boards_bp.route("", methods=['POST'])
def create_board():
    request_body = request.get_json()
    new_board = Board.from_dict(request_body)

    db.session.add(new_board)
    db.session.commit()

    # Give back our response
    return {
        "id": new_board.id,
        "title": new_board.title,
        "owner": new_board.owner,
        "msg": "Successfully created"
    }, 201


