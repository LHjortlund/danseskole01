from flask_restful import Resource, Api, reqparse
from typing_extensions import no_type_check

from models import db, Elev, Dansehold, hold_deltager, Stilart, Lokation, Instruktor, Registering

def register_api(app):
    api = Api(app)

    class ElevResource(Resource):
        def get(self, elev_id=None):
            if elev_id:
                elev = Elev.query.get(elev_id)
                if elev:
                    return {"navn": elev.fornavn, "fodselsdato": elev.fodselsdato}, 200
                return {"message": "Elev ikke fundet"}, 404
            elever = Elev.query.all()
            return [{"id": elev.id,
                     "fornavn": elev.fornavn,
                     "efternavn": elev.efternavn,
                     "fodselsdato": elev.fodselsdato,
                     "mobil": elev.mobil}
                    for elev in elever], 200

        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('fornavn', required=True)
            parser.add_argument('efternavn', required=True)
            parser.add_argument('fodselsdato', required=True)
            parser.add_argument('mobil', required=True)
            args = parser.parse_args()

            ny_elev = Elev(
                fornavn=args['fornavn'],
                efternavn=args['efternavn'],
                fodselsdato=args['fodselsdato'],
                mobil=args['mobil'])
            db.session.add(ny_elev)
            db.session.commit()
            return {"message": "Elev oprettet", "id": ny_elev.id}, 201

        def put(self, elev_id):
            elev = Elev.query.get(elev_id)
            if not elev:
                return {"message": "Elev ikke fundet"}, 404

            parser = reqparse.RequestParser()
            parser.add_argument('fornavn', required=False)
            parser.add_argument('efternavn', required=False)
            parser.add_argument('fodselsdato', required=False)
            parser.add_argument('mobil', required=False)
            args = parser.parse_args()

            if args['fornavn']:
                elev.fornavn = args['fornavn']
            if args['efternavn']:
                elev.efternavn = args['efternavn']
            if args['fodselsdato']:
                elev.fodselsdato = args['fodselsdato']
            if args['mobil']:
                elev.mobil = args['mobil']
            db.session.commit()

            return {"message": "Elev opdateret"}, 200

        def delete(self, elev_id):
            elev = Elev.query.get(elev_id)
            if not elev:
                return {"message": "Elev ikke fundet"}, 404

            db.session.delete(elev)
            db.session.commit()
            return {"message": "Elev slettet"}, 200

    api.add_resource(ElevResource, '/api/elever', '/api/elever/<int:elev_id>')

    class InstruktorResource(Resource):
        def get(self, instruktor_id=None):
            if instruktor_id:
                instruktor = Instruktor.query.get(instruktor_id)
                if instruktor:
                    return {"id": instruktor.id,
                            "fornavn": instruktor.fornavn,
                            "efternavn": instruktor.efternavn,
                            "mobil": instruktor.mobil,
                            "email": instruktor.email}, 200
                return {"message": "Instruktor ikke fundet"}, 404
            instruktors = Instruktor.query.all()
            return [{"id": i.id,
                     "fornavn": i.fornavn,
                     "efternavn": i.efternavn,
                     "email": i.email}
                    for i in instruktors], 200

    class DanseholdResource(Resource):
        def get(self, dansehold_id=None):
            if dansehold_id:
                dansehold = Dansehold.query.get(dansehold_id)
                if dansehold:
                    return {"id":dansehold.id,
                            "stilart":dansehold.stilart.stilart, #henter fra stilart
                            "instruktor":dansehold.instruktor,
                            "lokation":dansehold.lokation.adresse #henter fra lokation
                            }, 200
                return {"message": "Dansehold ikke fundet"}, 404
            dansehold_liste = Dansehold.query.all()
            return [{"id":dansehold.id,
                     "stilart":dansehold.stilart.stilart, #relateret felt
                     "instruktor":dansehold.instruktor} for dh in dansehold_liste], 200

        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('stilart_id', required=True)
            parser.add_argument('instruktor', required=False)
            parser.add_argument('lokation_id', required=True)
            args = parser.parse_args()

            nyt_dansehold = Dansehold(stilart=args['stilart_id'],
                                      instruktor=args('instruktor'),
                                      lokation_id=args['lokation_id'])

            db.session.add(nyt_dansehold)
            db.session.commit()
            return {"message": "Dansehold oprettet", "id": nyt_dansehold.id}, 201

        def put(self, dansehold_id):
            dansehold = Dansehold.query.get(dansehold_id)
            if not dansehold:
                return {"message": "Dansehold ikke fundet"}, 404

            parser = reqparse.RequestParser()
            parser.add_argument('stilart', required=False)
            parser.add_argument('instruktor', required=False)
            args = parser.parse_args()

            if args['stilart']:
                dansehold.stilart = args['stilart']
            if args['instruktor']:
                dansehold.instruktor = args['instruktor']
            db.session.commit()

            return {"message": "Dansehold opdateret"}, 200

        def delete(self, dansehold_id):
            dansehold = Dansehold.query.get(dansehold_id)
            if not dansehold:
                return {"message": "Dansehold ikke fundet"}, 404

            db.session.delete(dansehold)
            db.session.commit()
            return {"message": "Dansehold slettet"}, 200

    api.add_resource(DanseholdResource, '/api/dansehold', '/api/dansehold/<int:dansehold_id>')

    class StilartResource(Resource):
        def get(self, stilart_id=None):
            if stilart_id:
                stilart = Stilart.query.get(stilart_id)
                if stilart:
                    return {"id": stilart.id,
                            "stilart": stilart.stilart,
                            "beskrivelse": stilart.beskrivelse}, 200
                return {"message": "Stilart ikke fundet"}, 404

            stilarter = Stilart.query.all()
            return [{"id": s.id,
                     "stilart": s.stilart,
                     "beskrivelse": s.beskrivelse} for s in stilarter], 200

    api.add_resource(StilartResource, '/api/stilart', '/api/stilart/<int:stilart_id>')

    class RegisteringResource(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('elev_id', required=True)
            parser.add_argument('dansehold_id', required=True)
            args = parser.parse_args()

            elev = Elev.query.get(args['elev_id'])
            dansehold = Dansehold.query.get(args['dansehold_id'])
            if not elev or not dansehold:
                return {"message": "Elev eller dansehold ikke fundet"}, 404

            dansehold.registerings.append(Registering(elev_id=args['elev_id'], dansehold_id=args['dansehold_id']))
            db.session.commit()
            return {"message": "Elev tilføjet til dansehold"}, 200


    api.add_resource(RegisteringResource, '/api/registering')

