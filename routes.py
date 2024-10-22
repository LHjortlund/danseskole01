from flask import render_template, request
from models import Elev

def register_routes(app, db):
    @app.route('/')
    def index():
        elev = Elev.query.all()
        return str(elev)