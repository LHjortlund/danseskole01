from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from extensions import db
from models import Elev


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///danseskole.db'

    db.init_app(app)
    migrate = Migrate(app, db)
    return app

# @app.route('/')
# def home():
#     return render_template("index.html")



