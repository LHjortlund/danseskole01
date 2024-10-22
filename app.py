from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import Elev

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///danseskole.db'

    db.init_app(app)

    # Register routes here
    from routes import register_routes
    register_routes(app, db)

    migrate = Migrate(app, db)
    return app

    @app.route('/')
    def home():
        return render_template("index.html")

    return app