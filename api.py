from flask_restful import Resource, Api, reqparse
from typing_extensions import no_type_check

from models import Elev, db, Dansehold, Danselektion, attendance, Instruktor

def register_api(app):
    api = Api(app)

    class ElevResource(Resource):
        def get(self, elev_id=None):
            if elev_id:
                elev = Elev.query.get(elev_id)
                if elev:
                    return {"navn": elev.navn, "fodselsdato": elev.fodselsdato}, 200
                return {"message": "Elev ikke fundet"}, 404
            elever = Elev.query.all()
            return [{"id": elev.id, "navn": elev.navn, "fodselsdato": elev.fodselsdato} for elev in elever], 200

        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('navn', required=True)
            parser.add_argument('fodselsdato', required=True)
            args = parser.parse_args()

            ny_elev = Elev(navn=args['navn'], fodselsdato=args['fodselsdato'])
            db.session.add(ny_elev)
            db.session.commit()
            return {"message": "Elev oprettet", "id": ny_elev.id}, 201

        def put(self, elev_id):
            elev = Elev.query.get(elev_id)
            if not elev:
                return {"message": "Elev ikke fundet"}, 404

            parser = reqparse.RequestParser()
            parser.add_argument('navn', required=False)
            parser.add_argument('fodselsdato', required=False)
            args = parser.parse_args()

            if args['navn']:
                elev.navn = args['navn']
            if args['fodselsdato']:
                elev.fodselsdato = args['fodselsdato']
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
                    return {"id": instruktor.id, "navn": instruktor.navn, "email": instruktor.email}, 200
                return {"message": "Instruktor ikke fundet"}, 404
            instruktors = Instruktor.query.all()
            return [{"id": i.id, "navn": i.navn, "email": i.email} for i in instruktors], 200

    class DanseholdResource(Resource):
        def get(self, dansehold_id=None):
            if dansehold_id:
                dansehold = Dansehold.query.get(dansehold_id)
                if dansehold:
                    return {"id":dansehold.id,
                            "stilart":dansehold.stilart,
                            "instruktor":dansehold.instruktor,
                            "lokation":dansehold.lokation.navn
                            }, 200
                return {"message": "Dansehold ikke fundet"}, 404
            dansehold_liste = Dansehold.query.all()
            return [{"id":dansehold.id,
                     "stilart":dansehold.stilart,
                     "instruktor":dansehold.instruktor} for dh in dansehold_liste], 200

        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('stilart', required=True)
            parser.add_argument('instruktor', required=False)
            parser.add_argument('lokation_id', required=True)
            args = parser.parse_args()

            nyt_dansehold = Dansehold(stilart=args['stilart'],
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