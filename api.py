from flask_restful import Resource, Api, reqparse
from typing_extensions import no_type_check

from models import Elev, db

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
