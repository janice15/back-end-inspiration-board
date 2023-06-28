from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect, asc
from app.models.card import Card
from app import db
from app.routes.routes_helper import get_valid_item_by_id

# All routes defined with cards_bp start with url_prefix (/cards)
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    card_to_delete = get_valid_item_by_id(Card, card_id)

    db.session.delete(card_to_delete)
    db.session.commit()

    return f"Card {card_to_delete.message} is deleted!", 200

# patch route for likes count. 
@cards_bp.route("/<card_id>/like", methods=["PATCH"])
def patch_one_card(card_id):
    card_to_update = get_valid_item_by_id(Card, card_id)
    
    # update card likes count to increment by 1.
    card_to_update.likes_count += 1
    db.session.commit()
    return card_to_update.to_dict(), 200

