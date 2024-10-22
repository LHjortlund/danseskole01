from flask import render_template, request
from models import Elev

def register_routes(app, db):
    @app.route('/', )
    def index():
        elev = Elev.query.all()
        return str(elev)


    @app.route('/opret_elev', methods=["Get", "POST"])
    def opret_elev():
        navn = request.form.get('navn')
        fodselsdato = request.form.get('fodselsdato')
        if not navn or not fodselsdato:
            return "Fejl: Navn og fødselsdato skal udfyldes", 400

        ny_elev = Elev(navn=navn, fodselsdato=fodselsdato)
        db.session.add(ny_elev)
        db.session.commit()

        return "Elev oprettet!", 201

    @app.route('/elever', methods=['GET'])
    def hent_elever():
        elever = Elev.query.all()
        elev_liste = [{'id': elev.id, 'navn': elev.navn, 'fodselsdato': elev.fodselsdato} for elev in elever]
        return {"elever": elev_liste}

