from flask import render_template, request, redirect, url_for
from models import Elev, db, Dansehold, Danselektion, attendance

def register_routes(app, db):
    @app.route('/', )
    def index():
        return render_template('index.html')

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
            return redirect(url_for('elev'))
        return render_template('elev.html')

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
        return render_template('elev.html')

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
        return render_template('elev.html')

    @app.route('/dansehold')
    def dansehold():
        dansehold_liste = Dansehold.query.all() #Henter alle dansehold fra databasen
        lektioner = Danselektion.query.all() #henter alle danselektioner
        elever = Elev.query.all() #Tilføj elevliste
        return render_template('dansehold.html', dansehold_liste=dansehold_liste, lektioner=lektioner, elever=elever)

    @app.route('/opret_dansehold', methods=["GET", "POST"])
    def opret_dansehold():
        if request.method =="POST":
            stilart = request.form.get('stilart')
            instruktor = request.form.get('instruktor')
            lokation_id = request.form.get('lokation_id')
            nyt_dansehold = Dansehold(stilart=stilart, instruktor=instruktor, lokation_id=lokation_id)

            db.session.add(nyt_dansehold)
            db.session.commit()
            return redirect(url_for('dansehold'))
        return render_template('dansehold.html')

    @app.route('/danseholdene', methods=["GET"])
    def get_danseholdene():
        danseholdene = Dansehold.query.all() #modelname er 'Dansehold'
        dansehold_liste = [{"id": dansehold.id,
                            "stilart": dansehold.stilart,
                            "instruktor": dansehold.instruktor,
                            "lokation_id": dansehold.lokation_id.navn}
                           for dansehold in danseholdene]
        return {"danseholdene": dansehold_liste}, 200

    @app.route('/opdater_dansehold/<int:dansehold_id>', methods=["GET", "PUT"])
    def opdater_dansehold(dansehold_id):
        if request.method == "GET":
            dansehold = Dansehold.query.get(dansehold_id)
            if dansehold:
                return render_template('opdater_dansehold.html', dansehold=dansehold)
            return "Dansehold ikke fundet", 404

        if request.method == "PUT":
            data = request.get_json()
            dansehold = Dansehold.query.get(dansehold_id)
            if dansehold:
                dansehold.stilart = data.get("stilart", dansehold.stilart)
                dansehold.instruktor = data.get("instruktor", dansehold.instruktor)
                dansehold.lokation_id = data.get("lokation_id", dansehold.lokation_id)
                db.session.commit()
                return {"message": "Dansehold opdateret"}, 200
            return {"message": "Dansehold ikke fundet"}, 400
        return render_template('dansehold.html')

    @app.route('/slet_dansehold/<int:dansehold_id>', methods=["DELETE"])
    def slet_dansehold(dansehold_id):
        dansehold = Dansehold.query.get(dansehold_id)
        if dansehold:
            db.session.delete(dansehold)
            db.session.commit()
            return {"message": "Dansehold slettet"}, 200
        return {"message": "Dansehold blev ikke fundet og ikke slettet"}, 400

    @app.route('/tilfoej_elev_til_lektion/<int:lektion_id>', methods=["POST"])
    def tilfoej_elev_til_lektion(lektion_id):
        print("funktionen bliver kaldt")
        try:
            elev_id = request.form["elev_id"]
            print(f'Lektion ID: {lektion_id}, Elev ID: {elev_id}')
            #lektion_id = request.form.get("lektion_id")
            lektion = Danselektion.query.get(lektion_id)
            elev = Elev.query.get(elev_id)
            print("Lektion fundet:", lektion)
            print("Elev fundet:", elev)
            print("Funktion kaldt")
            print("Lektion ID fra URL:", lektion_id)
            print("Elev ID fra formular:", elev_id)

            if elev and lektion:
                lektion.attendance.append(elev)
                db.session.commit()
                return {"message": "Elev tilføjet til lektion"}, 200
            return {"message": "Elev eller lektion ikke fundet"}, 400

        except Exception as e:
            db.session.rollback()
            print(f"Fejl: {e}")
            return {"message": "Der opstod en fejl"}, 500


    # @app.route('/prøvetime')
    # def prøvetime():
    #     prøvetime_liste = Prøvetime.query.all()
    #     return render_template('prøvetime.html', prøvetime_liste=prøvetime_liste)
    #
    # @app.route('/opret_prøvetime', methods=["GET", "POST"])
    # def opret_prøvetime():
    #     if request.method == "POST":







