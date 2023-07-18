from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from sqlalchemy import inspect, asc

from app.models.card import Card
from app.models.board import Board
from app.routes.routes_helper import get_valid_item_by_id

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
#get  all boards
@boards_bp.route("", methods=['GET'])
def handle_boards():
    owner_query = request.args.get("owner")
    if owner_query:
        boards = Board.query.filter_by(owner=owner_query)
    else:
        boards = Board.query.all()

    boards_response = []
    for board in boards :
        boards_response.append(board.to_dict())
    return jsonify(boards_response), 200

#get single board
@boards_bp.route("/<board_id>", methods=['GET'])
def get_one_board(board_id):
    board = get_valid_item_by_id(Board, board_id)
    return board.to_dict(), 200



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

#get all cards for one board
@boards_bp.route("/<board_id>/cards", methods=['GET'])
def handle_cards(board_id):
    cards = Card.query.filter_by(board_id=board_id)
    cards_response = []
    for card in cards:
        cards_response.append(card.to_dict())

    return jsonify(cards_response), 200

#get a single card
@boards_bp.route("<board_id>/cards/<card_id>", methods=["GET"])
def handle_card(board_id, card_id):
    card = get_valid_item_by_id(Card, card_id)
    return card.to_dict(), 200

# Post a card to a board
@boards_bp.route("/<board_id>/cards", methods=['POST'])
def create_card(board_id):
    # Get the data from the request body
    request_body = request.get_json()
    updated_card_info = request_body
    new_card = Card.from_dict(request_body)

    # Use it to make an Card
    new_card= Card.from_dict(updated_card_info)

    # Persist (save, commit) it in the database
    db.session.add(new_card)
    db.session.commit()

    # Give back our response
    return {
        "card_id": new_card.card_id,
        "message": new_card.message,
        "likes_count": 0,
        "board_id": new_card.board_id,
        "msg": "Successfully created"
    }, 201


@boards_bp.route("/<board_id>/delete", methods=["DELETE"])
def delete_one_board(board_id):
    board_to_delete = get_valid_item_by_id(Board, board_id)

    db.session.delete(board_to_delete)
    db.session.commit()

    return f"Board {board_to_delete} is deleted!", 200