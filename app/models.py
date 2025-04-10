from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Bid(db.Model):
    __tablename__ = 'bids'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Bid {self.name}: {self.amount}>"


class Confirmation(db.Model):
    __tablename__ = 'confirmations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    def __repr__(self):
        return f"<Confirmed: {self.name}>"