from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Elev
from routes import register_routes

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///danseskole.db'
    db.init_app(app)

    migrate = Migrate(app, db)

    # Importer registrere routes og API
    from routes import register_routes
    from api import register_api
    register_routes(app)
    register_api(app)

    return app
