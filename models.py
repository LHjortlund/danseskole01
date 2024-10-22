from app import db
from flask_sqlalchemy import SQLAlchemy


class Elev(db.Model):
    __tabelname__ = 'Elev'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(100), nullable=False)
    fodselsdato = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'Elev {self.navn} og {self.fodselsdato}'
