from flask import Flask, request, jsonify

# Import der Datenbank-Modelle
from app.models import db, Bid, Confirmation

# Importierte Logik-Funktionen aus logic.py
from app.logic import (is_valid_name, is_valid_bid, save_or_update_bid)

from flask import Blueprint

# Blueprint erstellen, um die Routen von der App trennen
routes_blueprint = Blueprint("routes", __name__)

@routes_blueprint.route("/bid", methods=["POST"])
def place_bid():
    """Takes bids and saves them."""
    data = request.json
    name = data.get("name")
    amount = data.get("amount")

    if not name or not isinstance(name, str) or name.strip() == "":
        return jsonify({"error": "Invalid name!"}), 400

    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Your bid must be a positive number!"}), 400

    if not is_valid_name(name):
        return jsonify({"error": "Invalid name!"}), 400

    if not is_valid_bid(amount):
        return jsonify({"error": "Your bid must be a positive number!"}), 400

    result, current_amount = save_or_update_bid(name, amount)

    if result == "updated":
        return jsonify({"message": f"\nYour bid was successfully updated to {current_amount} $."})
    elif result == "lower_than_current":
        return jsonify({"message": f"\nYour new bid must be higher than your current bid of {current_amount} $."})
    else:
        return jsonify({"message": f"\nYour bid of {current_amount} $ was successfully placed."})


@routes_blueprint.route("/finish", methods=["POST"])
def finish_bidding():
    """Indicates that the bidder is done with bidding."""
    data = request.json
    name = data.get("name")

    if not name or name.strip() == "":
        return jsonify({"error": "Invalid name!"}), 400

    if not Confirmation.query.filter_by(name=name).first():
        db.session.add(Confirmation(name=name))
        db.session.commit()

    number_of_bidders = Bid.query.count()
    finished_confirmed = Confirmation.query.count()

    if finished_confirmed == number_of_bidders:
        return jsonify({"message": "\nAll bidders are done. The auction will end now."}), 200
    elif number_of_bidders == 0:
        return jsonify({"message": "\nNo bids were placed. The auction will end."}), 200
    else:
        return jsonify({"message": "\nWaiting for other bidders to finish bidding"}), 200


@routes_blueprint.route("/winner", methods=["GET"])
def get_winner():
    """Determines the winner from the bids."""
    number_of_bidders = Bid.query.count()
    finished_confirmed = Confirmation.query.count()

    if finished_confirmed != number_of_bidders:
        return jsonify({"error": "Not all bidders have finished yet."}), 400

    if number_of_bidders == 0:
        return jsonify({
            "winner": None,
            "amount": 0
        })

    max_bid_amount = db.session.query(db.func.max(Bid.amount)).scalar()
    highest_bidders = Bid.query.filter(Bid.amount == max_bid_amount).all()

    if len(highest_bidders) > 1:
        return jsonify({
            "tie": True,
            "amount": max_bid_amount,
            "bidders": [b.name for b in highest_bidders],
            "message": "Multiple bidders have the highest bid. They can now choose to raise their bids."
        }), 200

    winner = highest_bidders[0]
    response = jsonify({
        "winner": winner.name,
        "amount": winner.amount
    })

    return response


@routes_blueprint.route("/")
def home():
    return "Secret Auction Server is running"
