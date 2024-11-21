from flask import render_template, request, redirect, url_for
from models import db, Elev, Lokation, Dansehold, hold_deltager, Stilart, Instruktor, Registering
from datetime import datetime

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
            fornavn = request.form.get('fornavn')
            efternavn = request.form.get('efternavn')
            fodselsdato = request.form.get('fodselsdato')
            mobil = request.form.get('mobil')

            if not fornavn or not efternavn or not fodselsdato or not mobil:
                return "Fejl: Alle felter skal udfyldes", 400

            ny_elev = Elev(fornavn=fornavn, efternavn=efternavn, fodselsdato=fodselsdato, mobil=mobil)
            db.session.add(ny_elev)
            db.session.commit()
            return redirect(url_for('elev'))
        return render_template('elev.html')

    @app.route('/elever', methods=["GET"])
    def get_elever():
        elever = Elev.query.all()
        elev_liste = [{"id": elev.id,
                       "fornavn": elev.fornavn,
                       "efternavn": elev.efternavn,
                       "fodselsdato": elev.fodselsdato,
                       "mobil": elev.mobil} for elev in elever]
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
                elev.fornavn = data.get("fornavn", elev.fornavn)
                elev.efternavn = data.get("efternavn", elev.efternavn)
                elev.fodselsdato = data.get("fodselsdato", elev.fodselsdato)
                elev.mobil = data.get("mobil", elev.mobil)
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

    @app.route('/instruktor')
    def instruktor():
        instruktorer = Instruktor.query.all()
        return render_template('instruktor.html', instruktorer=instruktorer)

    @app.route('/opret_instruktor', methods=["POST"])
    def opret_instruktor():
        fornavn = request.form.get('fornavn')
        efternavn = request.form.get('efternavn')
        email = request.form.get('email')
        telefon = request.form.get('telefon')

        ny_instruktor = Instruktor(fornavn=fornavn, efternavn=efternavn, email=email, telefon=telefon)
        db.session.add(ny_instruktor)
        db.session.commit()
        return redirect(url_for('instruktor'))

    @app.route('/slet_instruktor/<int:instruktor_id>', methods=["DELETE"])
    def slet_instruktor(instruktor_id):
        instruktor = Instruktor.query.get(instruktor_id)
        if instruktor:
            db.session.delete(instruktor)
            db.session.commit()
            return {"message": "Instruktør slettet"}, 200
        return {"message": "Instruktør ikke fundet"}, 404

    @app.route('/dansehold')
    def dansehold():
        dansehold_liste = Dansehold.query.all() #Henter alle dansehold fra databasen
        instruktorer = Instruktor.query.all() #Henter alle instruktører
        elever = Elev.query.all() #Tilføj elevliste
        lokationer = Lokation.query.all()

        print(lokationer) #Debug - Tjek om listen ikke er tom
        return render_template('dansehold.html',
                               dansehold_liste=dansehold_liste,
                               elever=elever,
                               instruktorer=instruktorer,
                               lokationer=lokationer)

    @app.route('/opret_dansehold', methods=["GET", "POST"])
    def opret_dansehold():
        if request.method =="POST": #hent data fra formularen
            startdato = request.form.get('startdato')
            antal_gange = request.form.get('antal_gange')
            tidspunkt = request.form.get('tidspunkt')
            lokation = request.form.get('lokation_id')
            beskrivelse = request.form.get('beskrivelse')
            instruktor_id = request.form.get('instruktor_id')
            stilart_navn = request.form.get('stilart') #Henter tekstinput for stilart

            #Debug: Udskriv alle værdier
            print(f"startdato: {startdato}, antal_gange: {antal_gange}, tidspunkt: {tidspunkt}")
            print(f"lokation: {lokation}, instruktor_id: {instruktor_id}, stilart_navn: {stilart_navn}")


            # Konverter strenge til date og time objekter
            try:
                startdato = datetime.strptime(startdato, "%Y-%m-%d").date()
                tidspunkt = datetime.strptime(tidspunkt, "%H:%M").time()
            except ValueError as e:
                print(f"Fejl ved konvertering af dato/tidspunkt: {e}")
                return "Fejl: Forkert dato- eller tidsformat", 400

            # Validering og tjek for manglende input
            if (not startdato
                    or not antal_gange
                    or not tidspunkt
                    or not lokation
                    or not instruktor_id
                    or not stilart_navn):
                print("Fejl: Mindst ét felt er tomt!")
                return "Fejl: Alle felter skal udfyldes", 400

            #Tjek om stilart allerede finde, ellers oprettes den
            eksisterende_stilart = Stilart.query.filter_by(stilart=stilart_navn).first()
            if not eksisterende_stilart:
                ny_stilart =Stilart(stilart=stilart_navn, beskrivelse="Ingen beksrivelse angivet")
                db.session.add(ny_stilart)
                db.session.commit()
                stilart_id = ny_stilart.id
            else:
                stilart_id = eksisterende_stilart.id

            #Validering for manglende lokation
            # if not lokation:
            #     return "Fejl: Lokation ikke fundet", 400

            # Opret dansehold
            nyt_dansehold = Dansehold(
                startdato=startdato,
                antal_gange=antal_gange,
                tidspunkt=tidspunkt,
                lokation_id=int(lokation), #henter adresse for lokation
                beskrivelse=beskrivelse,
                instruktor_id=instruktor_id,
                stilart_id=stilart_id)

            db.session.add(nyt_dansehold)
            db.session.commit()
            return redirect(url_for('dansehold'))

        #Hent data til dropdowns
        stilarter = Stilart.query.all()
        instruktorer = Instruktor.query.all()
        lokationer = Lokation.query.all()
        print(lokationer) #til debugging: Læg mærke til om listen er tom
        return render_template('dansehold.html',
                               stilarter=stilarter,
                               instruktor=instruktorer,
                               lokationer=lokationer)

    @app.route('/danseholdene', methods=["GET"])
    def get_danseholdene():
        danseholdene = Dansehold.query.all() #modelname er 'Dansehold'
        dansehold_liste = [{"id": dansehold.id,
                            "stilart": dansehold.stilart,
                            "instruktor": dansehold.instruktor,
                            "lokation_id": dansehold.lokation_id.adresse}
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

    @app.route('/registrering', methods=["Get", "POST"])
    def registrer_elev():
        if request.method == "POST":
            elev_id = request.form.get('elev_id')
            dansehold_id = request.form.get('dansehold_id')

            elev = Elev.query.get(elev_id)
            dansehold = Dansehold.query.get(dansehold_id)

            if not elev or not dansehold:
                return "Fejl: Elev eller dansehold ikke fundet", 404

            registrering = Registering(dato=datetime.date.today(), elev_id=elev.id, dansehold_id=dansehold.id)
            db.session.add(registrering)
            db.session.commit()
            return redirect(url_for('registrer_elev'))

        dansehold = Dansehold.query.all()
        elever = Elev.query.all()
        registreringer = Registering.query.all()
        return render_template('registrering.html', dansehold=dansehold, elever=elever, registreringer=registreringer)

    # @app.route('/tilfoej_elev_til_lektion/<int:lektion_id>', methods=["POST"])
    # def tilfoej_elev_til_lektion(lektion_id):
    #     print("funktionen bliver kaldt")
    #     try:
    #         elev_id = request.form["elev_id"]
    #         print(f'Lektion ID: {lektion_id}, Elev ID: {elev_id}')
    #         #lektion_id = request.form.get("lektion_id")
    #         lektion = Danselektion.query.get(lektion_id)
    #         elev = Elev.query.get(elev_id)
    #         print("Lektion fundet:", lektion)
    #         print("Elev fundet:", elev)
    #         print("Funktion kaldt")
    #         print("Lektion ID fra URL:", lektion_id)
    #         print("Elev ID fra formular:", elev_id)
    #
    #         if elev and lektion:
    #             lektion.attendance.append(elev)
    #             db.session.commit()
    #             return {"message": "Elev tilføjet til lektion"}, 200
    #         return {"message": "Elev eller lektion ikke fundet"}, 400
    #
    #     except Exception as e:
    #         db.session.rollback()
    #         print(f"Fejl: {e}")
    #         return {"message": "Der opstod en fejl"}, 500


    # @app.route('/prøvetime')
    # def prøvetime():
    #     prøvetime_liste = Prøvetime.query.all()
    #     return render_template('prøvetime.html', prøvetime_liste=prøvetime_liste)
    #
    # @app.route('/opret_prøvetime', methods=["GET", "POST"])
    # def opret_prøvetime():
    #     if request.method == "POST":







