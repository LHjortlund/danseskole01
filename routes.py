from flask import render_template, request, redirect, url_for
from models import Elev, db

def register_routes(app, db):
    @app.route('/', )
    def index():
        elever = Elev.query.all()
        return render_template('index.html', elever=elever)

    @app.route('/elev')
    def elev():
        elever = Elev.query.all()  # Henter alle elever fra databasen
        return render_template('elev.html', elever=elever)

    @app.route('/opret_elev', methods=["GET", "POST"])
    def opret_elev():
        if request.method == "POST":
            navn = request.form.get('navn')
            fodselsdato = request.form.get('fodselsdato')
            if not navn or not fodselsdato:
                return "Fejl: Navn og fødselsdato skal udfyldes", 400

            ny_elev = Elev(navn=navn, fodselsdato=fodselsdato)
            db.session.add(ny_elev)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('index.html')

    @app.route('/elever', methods=["GET"])
    def get_elever():
        elever = Elev.query.all()
        elev_liste = [{"id": elev.id, "navn": elev.navn, "fodselsdato": elev.fodselsdato} for elev in elever]
        return {"elever": elev_liste}

    @app.route('/opdater_elev/<int:elev_id>', methods=["GET", "PUT"])
    def opdater_elev(elev_id):
        if request.method == "GET":
            elev = Elev.query.get(elev_id)
            if elev:
                return render_template('opdater_elev.html', elev= elev)
            return "Elev ikke fundet", 404

        if request.method == "PUT":
            data = request.get_json()
            elev = Elev.query.get(elev_id)
            if elev:
                elev.navn = data.get("navn", elev.navn)
                elev.fodselsdato = data.get("fodselsdato", elev.fodselsdato)
                db.session.commit()
                return {"message": "Elev opdateret"}, 200
            return {"message": "Elev ikke fundet"}, 400
        return render_template('index.html')

    @app.route('/slet_elev/<int:elev_id>', methods=["DELETE"])
    def slet_elev(elev_id):
        # if request.method == "GET":
        #     elev = Elev.query.get(elev_id)
        #     if elev:
        #         return render_template('slet_elev.html', elev= elev)
        #     return "Elev ikke fundet", 404

        if request.method == "DELETE":
            elev = Elev.query.get(elev_id)
            if elev:
                db.session.delete(elev)
                db.session.commit()
                return {"message": "Elev slettet"}, 200
            return {"message": "Elev ikke fundet og ikke slettet"}, 400
        return render_template('index.html')