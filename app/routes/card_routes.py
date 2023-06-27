from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect, asc
from app.models.card import Card
from app import db
from app.routes.routes_helper import get_valid_item_by_id

# All routes defined with cards_bp start with url_prefix (/cards)
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

@cards_bp.route("", methods=['GET'])
def handle_cards():
    name_query = request.args.get("name")
    if name_query:
        cards = Card.query.filter_by(name=name_query)
    else:
        cards = Card.query.order_by(asc(Card.card_id)).all()
    cards_response = []
    for card in cards:
        cards_response.append(card.to_dict())
    return jsonify(cards_response), 200

@cards_bp.route("", methods=['POST'])
def create_card():
    # Get the data from the request body
    request_body = request.get_json()

    # Use it to make an Card
    new_card= Card.from_dict(request_body)

    # Persist (save, commit) it in the database
    db.session.add(new_card)
    db.session.commit()

    # Give back our response
    return {
        "card_id": new_card.card_id,
        "message": new_card.message,
        "likes_count": new_card.likes_count,
        "board_id": new_card.board_id,
        "msg": "Successfully created"
    }, 201


@cards_bp.route("/<card_id>", methods=["GET"])
def handle_card(card_id):
    card = get_valid_item_by_id(Card, card_id)
    return card.to_dict(), 200


@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    card_to_delete = get_valid_item_by_id(Card, card_id)

    db.session.delete(card_to_delete)
    db.session.commit()

    return f"Card {card_to_delete.message} is deleted!", 200

# patch route for likes count. 
@cards_bp.route("/<card_id>", methods=["PATCH"])
def patch_one_card(card_id):
    card_to_update = get_valid_item_by_id(Card, card_id)
    
    # update card likes count to increment by 1.
    card_to_update.likes_count += 1
    db.session.commit()
    return card_to_update.to_dict(), 200
