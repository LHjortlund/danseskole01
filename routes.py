from flask import render_template, request, redirect, url_for
from models import Elev, db

def register_routes(app, db):
    @app.route('/', )
    def index():
        elever = Elev.query.all()
        return render_template('index.html', elever=elever)


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
        elev_liste = [{"navn": elev.navn, "fodselsdato": elev.fodselsdato} for elev in elever]
        return {"elever": elev_liste}





