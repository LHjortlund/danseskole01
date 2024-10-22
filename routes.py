from flask import render_template, request
from models import Elev

def register_routes(app, db):
    @app.route('/', )
    def index():
        elev = Elev.query.all()
        return str(elev)


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

            return "Elev oprettet!", 201

        return render_template('index.html')



