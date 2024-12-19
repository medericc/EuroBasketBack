from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

# Charger les variables depuis le fichier .env
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()



def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    
    # Initialiser db après avoir chargé la configuration
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
   

    # Importez et enregistrez les blueprints après l'initialisation de db
    from app.routes import players, teams, auth, games, transfers, users, events, career
    app.register_blueprint(players)
    app.register_blueprint(teams)
    app.register_blueprint(games)
    app.register_blueprint(transfers)
    app.register_blueprint(events)
    app.register_blueprint(career)
    app.register_blueprint(users)
    app.register_blueprint(auth)

    return app
