import os

from flask import Flask
from app.models import db, Bid, Confirmation  # Importiere die Datenbank-Modelle aus models.py
from app.routes import routes_blueprint  # Importiere die API-Endpunkte aus routes.py


def create_app():
    """
    Diese Factory-Funktion erstellt und konfiguriert die Flask-App.
    """
    # Erstelle die Flask-App
    app = Flask(__name__)

    # Absoluten Pfad zur Datenbank berechnen
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Aktuelles Verzeichnis ('/app')
    # Absoluter Pfad zur SQLite-Datenbank
    db_path = os.path.join(BASE_DIR, "auction.db")

    # SQLite-Datenbank-Konfigurationen
    # Absolute Pfadangabe
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    # Deaktiviere unnötige DB-Events (Performance)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialisiere die Datenbank
    db.init_app(app)
    with app.app_context():
        db.create_all()
        Bid.query.delete()
        Confirmation.query.delete()
        db.session.commit()

    # Registriere alle Routen (API-Endpunkte)
    app.register_blueprint(routes_blueprint)

    return app
