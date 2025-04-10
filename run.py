# Importiere die Factory-Funktion aus init.py
from app.init import create_app

# App erstellen mit der Factory-Funktion
app = create_app()

# Führe die App aus
if __name__ == "__main__":
    # Flask-Server starten; debug=True ist nur für Entwicklung!
    app.run(debug=True)
