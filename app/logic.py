from app.models import db, Bid, Confirmation


def is_valid_name(name):
    """Validates that name is non-empty and not longer than 10 characters."""
    return isinstance(name, str) and name.strip() != "" and len(name.strip()) <= 10


def is_valid_bid(amount):
    """Validates that bid is a positive number."""
    return isinstance(amount, (int, float)) and amount > 0


def save_or_update_bid(name, amount):
    existing_bid = Bid.query.filter_by(name=name).first()
    if existing_bid:
        if amount > existing_bid.amount:
            existing_bid.amount = amount
            db.session.commit()
            return "updated", existing_bid.amount
        else:
            return "lower_than_current", existing_bid.amount
    else:
        new_bid = Bid(name=name, amount=amount)
        db.session.add(new_bid)
        db.session.commit()
        return "new", amount


def confirm_bidding_done(name):
    if not Confirmation.query.filter_by(name=name).first():
        db.session.add(Confirmation(name=name))
        db.session.commit()


def all_bidders_done():
    return Bid.query.count() == Confirmation.query.count()


def get_winner_bid():
    if Bid.query.count() == 0:
        return None
    return Bid.query.order_by(Bid.amount.desc()).first()