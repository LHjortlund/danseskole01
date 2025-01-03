from flask import render_template, request, redirect, url_for, flash
from models import db, Elev, Lokation, Dansehold, hold_deltager, Stilart, Instruktor, Registering, Fremmøde
from datetime import datetime, date, timedelta
import logging

logging.basicConfig(level=logging.DEBUG)

# Hjælpefunktion til at generere datoer
def generer_datoer(startdato, antal_gange):
    datoer = []
    for i in range(antal_gange):
        datoer.append(startdato + timedelta(days=i*7))  # Fx hver uge
    return datoer

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

    @app.route('/registrer_elev', methods=["GET", "POST"])
    def registrer_elev():
        dansehold = Dansehold.query.all() #Henter alle dansehold
        elever = Elev.query.all() #Henter alle elever


        if request.method == "POST":
            dansehold_id = request.form.get('dansehold_id')
            elev_id = request.form.get('elev_id') #henter alle valgte elever (MULTIPLES)

            if not dansehold_id or not elev_id:
                flash("Vælg både dansehold og elev.", "danger")
            else:
                for elev_id in elev_id: #Tjek om elev allerede er tilmeldt danseholdet
                    eksisterende_registrering = Registering.query.filter_by(
                        dansehold_id=dansehold_id, elev_id=elev_id).first()
                    if eksisterende_registrering:
                        flash(f"Elev med ID {elev_id} er allerede tilmeldt danseholdet.", "warning")
                    else:
                        #opretter ny registrering
                        registrering = Registering(
                            dato=date.today(),
                            dansehold_id=dansehold_id,
                            elev_id=elev_id)
                        db.session.add(registrering)

                        #Opret Fremmøde automatisk for denne registerering
                        nyt_fremmoede = Fremmøde(
                            dato=registrering.dato,
                            elev_id=registrering.elev_id,
                            dansehold_id=registrering.dansehold_id,
                            registrering_id=registrering.id #Reference til den oprettede registrering
                        )
                        #Tilføj Fremmøde til sessionen
                        db.session.add(nyt_fremmoede)

            try:
                db.session.commit()  # Commit kun én gang
                flash("Registrering tilføjet!", "success")
            except Exception as e:
                db.session.rollback()  # Rul tilbage ved fejl
                flash(f"Fejl ved tilføjelse af registrering: {str(e)}", "danger")

        registreringer = Registering.query.all()  # Henter alle registreringer
        return render_template('registrering.html',
                               dansehold=dansehold,
                               registreringer=registreringer,
                               elever=elever,)

    @app.route('/slet_registrering_elev/<int:registrering_id>', methods=["POST"])
    def slet_registrering_elev(registrering_id):
        registrering = Registering.query.get_or_404(registrering_id)
        db.session.delete(registrering)
        db.session.commit()
        flash("Elev fjernet fra danseholdet.", "success")
        return redirect(url_for('registrer_elev'))

    @app.route('/fremmøde', methods=["GET"])
    def fremmoede_oversigt():
        dansehold = Dansehold.query.all() #Get all dansehold
        return render_template('fremmoede_oversigt.html', dansehold=dansehold)

    @app.route('/fremmøde/<int:dansehold_id>', methods=["GET", "POST"])
    def registrer_fremmoede(dansehold_id):
        # Hent dansehold og dets elever
        dansehold = Dansehold.query.get_or_404(dansehold_id)
        elever = dansehold.elever
        print("Elever:", elever)  # Log til kontrol
        print("Dansehold:", dansehold)  # Til debug
        print("Elever hentet for dansehold:", elever)  # Til debug

        # Generér datoer baseret på startdato og antal gange
        datoer = generer_datoer(dansehold.startdato, dansehold.antal_gange)

        # Initialiser fremmødedata (afkrydsning)
        fremmoede_data = {elev.id: {dato: False for dato in datoer} for elev in elever}
        print("Fremmøde data:", fremmoede_data)
        print("Elever:", elever)  # Tjek om elever er tom
        print("Datoer:", datoer)  # Tjek om datoer er korrekt genereret

        # Hent eksisterende fremmøder
        eksisterende_fremmoeder = Registering.query.filter_by(dansehold_id=dansehold_id).all()
        print("Eksisterende fremmøder:", eksisterende_fremmoeder)

        # Marker eksisterende fremmøder som `True`
        for fremmoede in eksisterende_fremmoeder:
            # Vi skal tjekke om både elev_id og dato findes i fremmoede_data
            if fremmoede.elev_id in fremmoede_data:
                if fremmoede.dato in fremmoede_data[fremmoede.elev_id]:
                    fremmoede_data[fremmoede.elev_id][fremmoede.dato] = True


        if request.method == "POST":
            print("Post request received!")
            print("Request form data:", request.form)
            # Processér data fra formularen
            for dato in datoer:
                for elev in elever:
                    fremmoede_key = f'fremmoede_{elev.id}_{dato.strftime("%Y-%m-%d")}'
                    fremmoede_checked = request.form.get(fremmoede_key) == "on"

                    eksisterende = Registering.query.filter_by(
                        dato=dato, elev_id=elev.id, dansehold_id=dansehold_id
                    ).first()

                    if fremmoede_checked and not eksisterende:
                        # Opret ny registrering
                        ny_registrering = Registering(
                            dato=dato,
                            elev_id=elev.id,
                            dansehold_id=dansehold_id
                        )
                        db.session.add(ny_registrering)
                    elif not fremmoede_checked and eksisterende:
                        # Slet eksisterende fremmøde
                        db.session.delete(eksisterende)

            db.session.commit()
            print("Ny registrering oprettet!")
            print(f"Elev ID: {elev.id}, Dato: {dato.strftime('%Y-%m-%d')}")

            flash("Fremmøde opdateret!", "success")
            return redirect(url_for('registrer_fremmoede', dansehold_id=dansehold_id))

        print("Opdateret fremmøde data:", fremmoede_data)

        return render_template(
            'fremmoede.html',
            dansehold=dansehold,
            datoer=datoer,
            fremmoede_data=fremmoede_data
        )

    @app.route('/opret_fremmoede', methods=['POST'])
    def opret_fremmoede():
        try:
            # Hent alle registreringer, som skal overføres til fremmøder
            registreringer = Registering.query.all()

            for registrering in registreringer:
                # Opret en ny Fremmøde-post
                nyt_fremmoede = Fremmøde(
                    dato=registrering.dato,
                    elev_id=registrering.elev_id,
                    dansehold_id=registrering.dansehold_id,
                    registering_id=registrering.id  # Reference til den originale registrering
                )
                db.session.add(nyt_fremmoede)

            # Gem ændringerne i databasen
            db.session.commit()
            return "Fremmøder oprettet fra registreringer!"
        except Exception as e:
            db.session.rollback()
            return f"Der opstod en fejl: {str(e)}"