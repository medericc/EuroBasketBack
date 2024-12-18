from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from app.routes import players, teams, games, transfers
    app.register_blueprint(players.bp)
    app.register_blueprint(teams.bp)
    app.register_blueprint(games.bp)
    app.register_blueprint(transfers.bp)

    return app
