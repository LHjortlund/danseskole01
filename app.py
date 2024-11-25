from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Elev, Dansehold, Registering
from routes import register_routes

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///danseskole.db'
    db.init_app(app)

    migrate = Migrate(app, db)

    # Importerer samt registrere routes og API
    from api import register_api
    register_routes(app, db)
    register_api(app)

    app.secret_key = 'en_meget_hemmelig_nøgle'  # Husk at denne skal skiftes til en unik værdi.

    return app
