from flask import Flask
from app.models import db  # Importiere die Datenbank-Modelle aus models.py
from app.routes import routes_blueprint  # Importiere die API-Endpunkte aus routes.py


def create_app():
    """
    Diese Factory-Funktion erstellt und konfiguriert die Flask-App.
    """
    app = Flask(__name__)  # Erstelle die Flask-App
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auction.db"  # SQLite-DB-Datei
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Deaktiviere unnötige DB-Events (Performance)

    # Initialisiere die Datenbank
    db.init_app(app)

    # Registriere alle Routen (API-Endpunkte)
    app.register_blueprint(routes_blueprint)

    return app